package main

import (
	"bufio"
	"flag"
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/goccy/go-graphviz"
	"github.com/goccy/go-graphviz/cgraph"
)

var (
	Path         string
	SubgraphSize float64
	Likelihood   float64
	TimeLimit    int
	Programs     []string

	NodeFunctionsComp []*NodeComp
	LineFunctionsComp []*FuncsComp

	Files [][]CodeLine = make([][]CodeLine, 2)
)

type EdgeType int
type NodeType int

type OppositeCodes struct {
	FileLeft  []CodeLine
	FileRight []CodeLine
}

type CodeLine struct {
	Line  string
	Color string
}

type NodeComp struct {
	Function int
	Comp     map[int]int
}

type FuncsComp struct {
	FirstLines  map[int]struct{}
	SecondLines map[int]struct{}
}

const (
	ControlEdge EdgeType = iota
	DataEdge
)

const (
	Root NodeType = iota
	Call
	Control // if, switch, for, while...
	Branch  // then, else ...
	Declaration
	Assignment
	Increment
	Return
	Expression
	Jump
	Label
	SwitchCase // case or default
	Another
	Count
)

// Определение класса Node по Label
func GetNodeType(inputLabel string) NodeType {
	label := strings.ToLower(inputLabel)
	controlRe := regexp.MustCompile(`^.*((if)|(for)|(while)).*$`)
	branchRe := regexp.MustCompile(`^.*((then)|(else)|(loop)).*$`)
	incrementRe := regexp.MustCompile(`^(.*\+\+.*)|(.*--.*)|(.*\+=.*)|(.*-=.*)|(.*/=.*)|(.*\*=.*)$`)
	expressionRe := regexp.MustCompile(`^.*[+\-*/%^~].*$`)
	callRe := regexp.MustCompile(`^\w+\(.*\)$`)
	returnRe := regexp.MustCompile(`^.*return.*$`)
	assignRe := regexp.MustCompile(`^\w+\s*=\s*.*$`)
	switch {
	case controlRe.MatchString(label):
		return Control
	case branchRe.MatchString(label):
		return Branch
	case incrementRe.MatchString(label):
		return Increment
	case expressionRe.MatchString(label):
		return Expression
	case callRe.MatchString(label):
		return Call
	case returnRe.MatchString(label):
		return Return
	case assignRe.MatchString(label):
		return Assignment
	default:
		return Another
	}
}

type Edge struct {
	Destination *Node
	Type        EdgeType
}

type Node struct {
	Type   NodeType
	Number int
	Edges  []*Edge
	Label  string
	Name   string
	Start  int
	End    int
}

func ParseArgs() {
	subgraphSize := flag.Float64("s", 0.9, "minimum common subgraph size")
	timeLimit := flag.Int("t", 10, "time limit on subgraph isomorphism")
	likelihoodLevel := flag.Float64("l", 0.995, "level of likelihood")
	program1 := flag.String("p1", "", "first program")
	program2 := flag.String("p2", "", "second program")
	flag.Parse()

	TimeLimit = *timeLimit
	SubgraphSize = *subgraphSize
	Likelihood = *likelihoodLevel
	Programs = []string{*program1, *program2}
}

func main() {
	//if len(os.Args) < 3 {
	//	log.Fatal("usage: ./graph_checker -p1=program1 -p2=program2")
	//}
	ParseArgs()

	//files := Files
	//fmt.Println(files)

	http.HandleFunc("/check", func(w http.ResponseWriter, r *http.Request) {
		Programs = []string{
			strings.TrimSpace(r.URL.Query().Get("p1")),
			strings.TrimSpace(r.URL.Query().Get("p2")),
		}

		now := time.Now()
		Check()
		fmt.Printf("Working %v seconds\n", int(time.Since(now).Seconds()))

		tmpl, err := template.New("tmpl").Parse(temple)
		if err != nil {
			log.Fatal(err)
		}
		err = tmpl.Execute(w, OppositeCodes{
			FileLeft:  Files[0],
			FileRight: Files[1],
		})
		if err != nil {
			log.Fatal(err)
		}
	})

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		tmpl, err := template.New("start").Parse(startTemple)
		if err != nil {
			log.Fatal(err)
		}
		err = tmpl.Execute(w, nil)
		if err != nil {
			log.Fatal(err)
		}
	})

	fmt.Println("http://127.0.0.1:8181")
	err := http.ListenAndServe(":8181", nil)
	if err != nil {
		log.Fatal(err)
	}
}

func Check() {
	var err error
	Path, err = os.Getwd()
	if err != nil {
		log.Fatal(err)
	}
	pathGraphs := Path + "/temp/"

	nodesAll := make([][][]*Node, 2)

	for i, program := range Programs {
		file, err := os.Open(program)
		if err != nil {
			log.Fatal(err)
		}
		defer func() {
			if err = file.Close(); err != nil {
				log.Fatal(err)
			}
		}()

		b, err := ioutil.ReadAll(file)
		if err != nil {
			log.Fatal(err)
		}
		lines := strings.Split(string(b), "\n")
		for _, line := range lines {
			Files[i] = append(Files[i], CodeLine{
				Line:  line,
				Color: "#000000",
			})
		}
	}

	for i := range nodesAll {
		cmd := exec.Command(Path+"/PyDG/parser.py", Programs[i])

		pathDot := fmt.Sprintf("%s/temp/test%v.dot", Path, i+1)
		outfile, err := os.Create(pathDot)
		if err != nil {
			log.Fatal(err)
		}
		defer outfile.Close()
		cmd.Stdout = outfile

		err = cmd.Start()
		if err != nil {
			log.Fatal(err)
		}
		err = cmd.Wait()
		if err != nil {
			log.Fatal(err)
		}
		nodesAll[i], err = ParsePDG(pathDot)
		if err != nil {
			log.Fatal(err)
		}
	}

	for i, nodes := range nodesAll {
		graph := StringifyNodes(nodes)

		// open output file
		fo, err := os.Create(pathGraphs + fmt.Sprintf("graph%v.txt", i+1))
		if err != nil {
			log.Fatal(err)
		}
		// make a write buffer
		w := bufio.NewWriter(fo)
		_, err = w.Write([]byte(graph))
		if err != nil {
			log.Fatal(err)
		}

		err = w.Flush()
		if err != nil {
			log.Fatal(err)
		}
		// close fo on exit and check for its returned error
		if err := fo.Close(); err != nil {
			log.Fatal(err)
		}
	}

	b, err := exec.Command(
		Path+"/PyMCIS/run.py",
		Path+"/temp/graph1.txt",
		Path+"/temp/graph2.txt",
		fmt.Sprint(SubgraphSize),
		fmt.Sprint(TimeLimit),
		fmt.Sprint(Likelihood)).
		Output()
	if err != nil {
		log.Fatal(err)
	}
	for _, line := range strings.Split(string(b), "\n") {
		elems := strings.Split(line, " ")
		if len(elems) == 4 {
			i1, _ := strconv.Atoi(elems[0])
			i2, _ := strconv.Atoi(elems[1])
			likely, _ := strconv.ParseFloat(elems[2], 64)
			ParseNodesComp(i1, i2, elems[3])
			if likely >= 0.0 {
				fmt.Printf(
					"%s vs %s: %v\n",
					PrettifyFuncName(nodesAll[0][i1][0].Label),
					PrettifyFuncName(nodesAll[1][i2][0].Label),
					likely,
				)
			}
		} else if len(elems) == 1 {
			plag, _ := strconv.ParseFloat(elems[0], 64)
			fmt.Println("Plagiarism:", plag)
			break
		}
	}

	thisComp := NodeFunctionsComp
	fmt.Println(thisComp)
	for i, comp := range NodeFunctionsComp {
		linesComp1 := make(map[int]struct{}, len(comp.Comp))
		linesComp2 := make(map[int]struct{}, len(comp.Comp))
		for k, v := range comp.Comp {

			start, end := nodesAll[0][i][k].Start, nodesAll[0][i][k].End
			if start != -1 && end != -1 {
				for j := start; j <= end; j++ {
					linesComp1[j] = struct{}{}
					Files[0][j-1].Color = "#FF0000"
				}
			}
			start, end = nodesAll[1][comp.Function][v].Start, nodesAll[1][comp.Function][v].End
			if start != -1 && end != -1 {
				for j := start; j <= end; j++ {
					linesComp2[j] = struct{}{}
					Files[1][j-1].Color = "#FF0000"
				}
			}
		}
		LineFunctionsComp = append(LineFunctionsComp, &FuncsComp{
			FirstLines:  linesComp1,
			SecondLines: linesComp2,
		})
	}
}

func ParseNodesComp(i1, i2 int, comp string) {
	pairs := strings.Split(comp[1:len(comp)-1], ",")

	fmt.Println(pairs)
	compMap := make(map[int]int, len(pairs))
	for _, pair := range pairs {
		if len(pair) == 0 {
			continue
		}
		kv := strings.Split(pair, ":")
		k, _ := strconv.Atoi(kv[0])
		v, _ := strconv.Atoi(kv[1])
		compMap[k] = v
	}
	NodeFunctionsComp = append(NodeFunctionsComp, &NodeComp{
		Function: i2,
		Comp:     compMap,
	})
}

func ParsePDG(path string) ([][]*Node, error) {
	b, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}
	graph, err := graphviz.ParseBytes(b)
	if err != nil {
		return nil, err
	}
	allNodes := make([][]*Node, 0, graph.NumberSubGraph())
	for i := 0; i < graph.NumberSubGraph(); i++ {
		sub := graph.SubGraph(fmt.Sprintf("sub_%v", i), 0)
		if sub == nil || sub.NumberNodes() == 0 {
			continue
		}
		nodesMap := CreateGraph(sub)
		nodes := ReduceNodes(nodesMap)
		if len(nodes) != 0 {
			allNodes = append(allNodes, nodes)
		}
	}
	return allNodes, nil
}

func ReduceNodes(nodesMap map[string]*Node) []*Node {
	var nodes []*Node
	nodesIndex := make(map[int]*Node, len(nodesMap))
	for _, node := range nodesMap {
		nodesIndex[node.Number] = node
	}
	for i := 0; i < len(nodesIndex); i++ {
		node, ok := nodesIndex[i]
		if !ok {
			j := 1
			for !ok {
				node, ok = nodesIndex[i+j]
				j++
			}
		}
		nodes = append(nodes, node)
	}
	return nodes
}

func CreateGraph(graph *cgraph.Graph) map[string]*Node {
	graphNode := graph.FirstNode() // Первая Node всегда "Root"
	parts := strings.Split(graphNode.Get("label"), "$")
	label := parts[0]
	start, end := -1, -1
	var err error
	if len(parts) > 1 {
		lineNoParts := strings.Split(parts[1], ":")
		start, err = strconv.Atoi(lineNoParts[0])
		if err != nil {
			start, end = -1, -1
		} else {
			if len(lineNoParts) > 1 {
				end, err = strconv.Atoi(lineNoParts[1])
			}
			if err != nil || len(lineNoParts) <= 1 {
				end = start
			}
		}
	}
	node := &Node{
		Type:   Root,
		Number: 0,
		Label:  label,
		Start:  start,
		End:    end,
		Name:   graphNode.Name(),
	}
	nodes := make(map[string]*Node, graph.NumberNodes())
	nodes[graphNode.Name()] = node
	AddNodes(graph, graphNode, node, nodes, nil)
	return nodes
}

func AddNodes(graph *cgraph.Graph, rootNodeGraph *cgraph.Node, node *Node, nodes map[string]*Node, baseNode *Node) {
	actual := true
	curEdgeGraph := graph.FirstOut(rootNodeGraph)
	if curEdgeGraph == nil {
		return
	}
	curNodeGraph := curEdgeGraph.Node()
	if curNodeGraph == nil {
		return
	}
	curNodeName := curNodeGraph.Name()
	if _, ok := nodes[curNodeName]; ok {
		actual = false
	}

	for {
		var curNode *Node
		if actual {
			parts := strings.Split(curNodeGraph.Get("label"), "$")
			label := parts[0]
			start, end := -1, -1
			var err error
			if len(parts) > 1 {
				lineNoParts := strings.Split(parts[1], ":")
				start, err = strconv.Atoi(lineNoParts[0])
				if err != nil {
					start, end = -1, -1
				} else {
					if len(lineNoParts) > 1 {
						end, err = strconv.Atoi(lineNoParts[1])
					}
					if err != nil || len(lineNoParts) <= 1 {
						end = start
					}
				}
			}
			curNode = &Node{
				Type:   GetNodeType(label),
				Number: len(nodes),
				Label:  label,
				Start:  start,
				End:    end,
				Name:   curNodeName,
			}
			nodes[curNodeGraph.Name()] = curNode

			AddNodes(graph, curNodeGraph, curNode, nodes, node)
		} else {
			curNode = nodes[curNodeGraph.Name()]
		}
		edgeType := ControlEdge
		if curEdgeGraph.Get("style") == "dotted" {
			edgeType = DataEdge
		}
		node.Edges = append(node.Edges, &Edge{
			Destination: curNode,
			Type:        edgeType,
		})

		curEdgeGraph = graph.NextEdge(curEdgeGraph, rootNodeGraph)
		if curEdgeGraph == nil {
			return
		}
		curNodeGraph = curEdgeGraph.Node()
		if curNodeGraph == nil {
			return
		}
		curNodeName = curNodeGraph.Name()
		if baseNode != nil && baseNode.Name == curNodeName {
			return
		}
		if _, ok := nodes[curNodeName]; ok {
			actual = false
		} else {
			actual = true
		}
	}
}

func StringifyNodes(nodesAll [][]*Node) string {
	output := "t\n"
	for _, nodes := range nodesAll {
		for i, node := range nodes {
			output += fmt.Sprintf("v %v %v\n", i, node.Type)
		}
		for i, node := range nodes {
			for _, edge := range node.Edges {
				if i == edge.Destination.Number {
					continue
				}
				output += fmt.Sprintf("e %v %v %v\n", i, edge.Destination.Number, edge.Type)
			}
		}
		output += "t\n"
	}
	return output
}

func PrettifyFuncName(label string) string {
	return fmt.Sprintf("%60s     ", label[10:])
}

var startTemple = `
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>/api/tarantool/</title>
</head>
<style type="text/css">
	* {
		font-family: "Helvetica", sans-serif;
		margin: 0;
		padding: 0;
	}

	.container {
		display: flex;
	}

	.left, .right {
		min-width: 30%;
		word-break: break-all;
		flex-grow: 1;
	}

	.base_block {
		margin-top: 10px;
	}

	.error {
		color: #dc143c;
		margin-top: 10px;
	}

	.response {
		font-family: "Fira Mono", monospace;
		font-size: 12px;
		border: 1px solid;
		border-radius: 5px;
		padding: 10px;
		display: inline-block;
	}

	.mb {
		margin-bottom: 5px;
	}

	body {
		margin: 10px;
	}

	h3 {
		margin-bottom: 5px;
	}

	h5 {
		margin-bottom: 5px;
	}
</style>
<body>
<h3>Input</h3>
<form action="/check" method="GET">
	<div class="mb">
		<input type="text" name="p1" style="width: 20em">
		<input type="text" name="p2" style="width: 20em">
	</div>
	<div>
		<input type="submit" value="Проверить!"/>
	</div>
</form>
</body>
</html>`

var temple = `<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>/api/tarantool/</title>
</head>
<style type="text/css">
	* {
		font-family: "Helvetica", sans-serif;
		margin: 0;
		padding: 0;
	}

	.container {
		display: flex;
	}

	.left, .right {
		min-width: 30%;
		word-break: break-all;
		flex-grow: 1;
	}

	.base_block {
		margin-top: 10px;
	}

	.error {
		color: #dc143c;
		margin-top: 10px;
	}

	.response {
		font-family: "Fira Mono", monospace;
		font-size: 12px;
		border: 1px solid;
		border-radius: 5px;
		padding: 10px;
		display: inline-block;
	}

	.mb {
		margin-bottom: 5px;
	}

	body {
		margin: 10px;
	}

	h3 {
		margin-bottom: 5px;
	}

	h5 {
		margin-bottom: 5px;
	}
</style>
<body>
<h3>Plagiarism</h3>
		<div class="container">
			<div class="left">
				<div class="response">
				{{range .FileLeft}}
					<p style="color:{{.Color}};">
						{{.Line}}
					</p>
				{{end}}
				</div>
			</div>
			<div class="right">
				<div class="response">
				{{range .FileRight}}
					<p style="color:{{.Color}};">
						{{.Line}}
					</p>
				{{end}}
				</div>
			</div>
		</div>
</body>
`
