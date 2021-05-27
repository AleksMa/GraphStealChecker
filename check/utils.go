package check

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"

	"github.com/goccy/go-graphviz"
	"github.com/goccy/go-graphviz/cgraph"
)

func ParseNodesComp(i1, i2 int, comp string) *NodeComp {
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
	return &NodeComp{
		Function: i2,
		Comp:     compMap,
	}
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
