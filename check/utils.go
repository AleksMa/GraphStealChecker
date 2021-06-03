package check

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

// Текстовые утилиты

// Преобразование внутреннего формата PDG в формат, понятный PyMCS
// t
// v <vertex_number> <vertex_attribute>
// vertexes...
// e <edge_source> <edge_dest> <edge_attribute>
// edges...
// t
// another subgraphs...
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

func WriteInnerGraph(pathGraphs string, nodesAll [][][]*Node) {
	for i, nodes := range nodesAll {
		graph := StringifyNodes(nodes)

		fo, err := os.Create(pathGraphs + fmt.Sprintf("graph%v.txt", i+1))
		if err != nil {
			log.Fatal("txt output: ", err)
		}

		w := bufio.NewWriter(fo)
		_, err = w.Write([]byte(graph))
		if err != nil {
			log.Fatal("txt output: ", err)
		}

		err = w.Flush()
		if err != nil {
			log.Fatal("txt output: ", err)
		}

		if err := fo.Close(); err != nil {
			log.Fatal("txt output: ", err)
		}
	}
}

// "Красивая" запись имени функции
func PrettifyFuncName(label string) string {
	return fmt.Sprintf("%60s     ", label[10:])
}
