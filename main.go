package main

import (
	"bufio"
	"bytes"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"

	"github.com/goccy/go-graphviz"
	"github.com/goccy/go-graphviz/cgraph"
)

var Path string
var SubgraphSize float64
var Likelihood float64

type EdgeType int
type NodeType int

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

func GetOmega(nodes []*Node) []float64 {
	omega := make([]float64, Count)
	for _, node := range nodes {
		omega[node.Type]++
	}
	for i := range omega {
		omega[i] /= float64(len(nodes))
	}
	return omega
}

func GetTau(nodes []*Node, omega []float64) float64 {
	m := make([]int, Count)
	for _, node := range nodes {
		m[node.Type]++
	}

	fmt.Println(m)
	fmt.Println(omega)

	tau := 0.0
	for i := range omega {
		if m[i] == 0 || omega[i] == 0 {
			continue
		}
		tau += 2 * float64(m[i]) * math.Log(float64(m[i])/(float64(len(nodes))*omega[i]))
	}
	return tau
}

func TestLikelihood(nodesFirst, nodesSecond []*Node) (bool, float64) {
	omega := GetOmega(nodesFirst)
	tau := GetTau(nodesSecond, omega)

	cmd := exec.Command(Path+"/chi_square.py", fmt.Sprint(Likelihood), strconv.Itoa(int(Count)))
	out, err := cmd.Output()
	if err != nil {
		log.Fatal(err)
	}
	prob, err := strconv.ParseFloat(strings.Split(string(out), "\n")[0], 64)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("tau & prob:", tau, prob)
	return math.Abs(tau) < prob, tau
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
}

var (
	nodesSlice []*Node
)

func main() {
	if len(os.Args) < 3 {
		log.Fatal("usage: ./graph_checker program1 program2")
	}

	subgraphSize := flag.Float64("s", 0.9, "minimum common subgraph size")
	likelihoodLevel := flag.Float64("l", 0.995, "minimum common subgraph size")
	program1 := flag.String("p1", "", "first program")
	program2 := flag.String("p2", "", "second program")
	flag.Parse()

	SubgraphSize = *subgraphSize
	Likelihood = 1 - *likelihoodLevel

	Path, _ = filepath.Abs(filepath.Dir(os.Args[0]))
	pathGraphs := Path + "/data/"
	programs := []string{*program1, *program2}

	nodesAll := make([][][]*Node, 2, 2)

	for i := 0; i < 2; i++ {
		//pathInput := "./data/test.py"
		cmd := exec.Command(Path+"/PyDG/parser.py", programs[i])
		// open the out file for writing

		pathDot := fmt.Sprintf("%s/data/test%v.dot", Path, i+1)
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

	commonPlag := 0.0
	firstSize, secondSize := 0, 0
	for i, subgraphFirst := range nodesAll[0] {
		firstSize += len(subgraphFirst)
		maxPlag := 0.0
		maxJ := 0
		for j, subgraphSecond := range nodesAll[1] {
			if i == 0 {
				secondSize += len(subgraphSecond)
			}
			likelihood, _ := TestLikelihood(subgraphFirst, subgraphSecond)
			if !likelihood || float64(len(subgraphFirst)) / float64(len(subgraphSecond)) < 0.9 || float64(len(subgraphFirst)) / float64(len(subgraphSecond)) > 1.1 {
				continue
			}
			//if tau == 0 {
			//	maxPlag = 2 * float64(len(subgraphSecond)) / float64(len(subgraphFirst)+len(subgraphSecond))
			//	maxJ = j
			//	continue
			//}
			for k, nodes := range [][]*Node{subgraphFirst, subgraphSecond} {
				graph := PrintNodes(nodes)

				// open output file
				fo, err := os.Create(pathGraphs + fmt.Sprintf("graph%v.txt", k+1))
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

			fmt.Println(SubgraphSize)
			b, err := exec.Command(Path+"/PyMCIS/run.py", Path+"/data/graph1.txt", Path+"/data/graph2.txt", fmt.Sprint(SubgraphSize), "10.").Output()
			if err != nil {
				log.Fatal(err)
			}

			res := bytes.Split(b, []byte("\n"))
			if len(res) == 0 {
				log.Fatal("Unexpected res: ", string(b))
			}

			plag, err := strconv.Atoi(string(res[0]))
			if err != nil {
				log.Fatal(err)
			}
			plagF := 2 * float64(plag) / float64(len(subgraphFirst)+len(subgraphSecond))
			if plagF > maxPlag {
				maxPlag = plagF
				maxJ = j
			}
		}
		commonPlag += maxPlag * (float64(len(nodesAll[1][maxJ]) + len(nodesAll[0][i])))
	}
	fmt.Println("Plagiarism: ", commonPlag/float64(len(nodesAll[0])))
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
		//fmt.Println(sub.)
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
	// TODO: reducing
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
	node := &Node{
		Type:   Root,
		Number: 0,
		Label:  "Root",
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
			label := curNodeGraph.Get("label")
			curNode = &Node{
				Type:   GetNodeType(label),
				Number: len(nodes),
				Label:  label,
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
		//fmt.Println(curEdgeGraph.Node().Name(), "\n\n")
		//if curEdgeGraph.Node().Name() == "a89110b0-951f-4d08-897a-89227c5761d7" {
		//	fmt.Println("get")
		//}
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

func PrintNodes(nodes []*Node) string {
	output := ""
	for i, node := range nodes {
		output += fmt.Sprintf("v %v %v\n", i, node.Type)
	}
	for i, node := range nodes {
		for _, edge := range node.Edges {
			output += fmt.Sprintf("e %v %v %v\n", i, edge.Destination.Number, edge.Type)
		}
	}
	return output
}
