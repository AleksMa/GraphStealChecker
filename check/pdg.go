package check

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"strconv"
	"strings"

	"github.com/goccy/go-graphviz"
	"github.com/goccy/go-graphviz/cgraph"
)

// Инструментарий преобразования dot-формата PDG во внутреннее представление

// Парсер dot-формата
func CreateNodesSet(path string, programs []string, codeLines [][]CodeLine) [][][]*Node {
	nodesAll := make([][][]*Node, 2)

	for i := range nodesAll {
		cmd := exec.Command(path+"/PyDG/parser.py", programs[i])

		pathDot := fmt.Sprintf("%s/temp/test%v.dot", path, i+1)
		outfile, err := os.Create(pathDot)
		if err != nil {
			log.Fatal("parser: ", err)
		}
		defer outfile.Close()
		cmd.Stdout = outfile

		err = cmd.Start()
		if err != nil {
			log.Fatal("parser: ", err)
		}
		err = cmd.Wait()
		if err != nil {
			log.Fatal("parser: ", err)
		}
		nodesAll[i], err = ParsePDG(pathDot, &(codeLines[i]))
		if err != nil {
			log.Fatal("parser: ", err)
		}
	}
	return nodesAll
}

// Выделение связных компонент в PDG
func ParsePDG(path string, file *[]CodeLine) ([][]*Node, error) {
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
		nodesMap := CreateGraph(sub, file)
		nodes := ReduceNodes(nodesMap)
		if len(nodes) != 0 {
			allNodes = append(allNodes, nodes)
		}
	}
	return allNodes, nil
}

// Конструктор связной компоненты
func CreateGraph(graph *cgraph.Graph, file *[]CodeLine) map[string]*Node {
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
	if start != -1 {
		if end == -1 {
			(*file)[start-1].Parsed = true
		} else {
			for i := start - 1; i <= end-1; i++ {
				(*file)[i].Parsed = true
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

// Рекурсивная функция добавления узлов во внутреннее представление
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

// Перенумерация вершин "расширенными" натуральными числами (начиная с нуля)
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
