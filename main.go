package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"

	"github.com/goccy/go-graphviz"
	"github.com/goccy/go-graphviz/cgraph"
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
	Declaration
	Assignment
	Increment
	Return
	Expression
	Jump
	Label
	SwitchCase // case or default
	Another
)

func GetNodeType(inputLabel string) NodeType {
	label := strings.ToLower(inputLabel)
	controlRe := regexp.MustCompile(`^((if)|(for)|(while)).+$`)
	assignRe := regexp.MustCompile(`^\w.+ = .*$`)
	switch {
	case controlRe.MatchString(label):
		return Control
	case assignRe.MatchString(label):
		return Control
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

var (
	nodesSlice []*Node
)

func main() {
	if len(os.Args) < 3 {
		log.Fatal("usage: ./graph_checker program1 program2")
	}

	path, _ := filepath.Abs(filepath.Dir(os.Args[0]))
	pathGraphs := path + "/data/"
	programs := os.Args[1:]

	nodesAll := make([][][]*Node, 2, 2)

	for i := 0; i < 2; i++ {
		//pathInput := "./data/test.py"
		cmd := exec.Command(path+"/PyDG/parser.py", programs[i])
		// open the out file for writing

		pathDot := fmt.Sprintf("%s/data/test%v.dot", path, i+1)
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
	for _, subgraphFirst := range nodesAll[0] {
		maxPlag := 0.0
		for _, subgraphSecond := range nodesAll[1] {
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

			b, err := exec.Command(path+"/PyMCIS/run.py", path+"/data/graph1.txt", path+"/data/graph2.txt", "0.9").Output()
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
			plagF := 2 * float64(plag) / float64(len(subgraphFirst) + len(subgraphSecond))
			if plagF > maxPlag {
				maxPlag = plagF
			}
		}
		commonPlag += maxPlag
	}
	fmt.Println("Plagiarism: ", commonPlag / float64(len(nodesAll[0])))
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
				Type:   GetNodeType(label), //FIXME
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
