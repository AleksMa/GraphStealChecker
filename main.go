package main

import (
	"bufio"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
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
)

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
	now := time.Now()
	if len(os.Args) < 3 {
		log.Fatal("usage: ./graph_checker -p1=program1 -p2=program2")
	}
	ParseArgs()

	var err error
	Path, err = os.Getwd()
	if err != nil {
		log.Fatal(err)
	}
	pathGraphs := Path + "/temp/"

	nodesAll := make([][][]*Node, 2)

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
		if len(elems) == 3 {
			i1, _ := strconv.Atoi(elems[0])
			i2, _ := strconv.Atoi(elems[1])
			likely, _ := strconv.ParseFloat(elems[2], 64)
			if likely != 0.0 {
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

	fmt.Printf("Working %v seconds\n", int(time.Since(now).Seconds()))
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
		Label:  graphNode.Get("label"),
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
	return label[10:]
}
