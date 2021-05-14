package main

import (
	"fmt"
	"io/ioutil"
	"log"

	"github.com/goccy/go-graphviz"
)

func main() {
	path := "./test/test.dot"
	b, err := ioutil.ReadFile(path)
	if err != nil {
		log.Fatal(err)
	}
	graph, err := graphviz.ParseBytes(b)
	if err != nil {
		fmt.Println(err)
		return
	}
	sub := graph.SubGraph("sub_1", 0)
	node := sub.FirstNode()
	//node, err := sub.Node("c52c8673-ee1a-42eb-a2de-ad12439fc0c1")
	fmt.Println(node.Get("label"))
	fmt.Println(sub.FirstOut(node).Node().Get("label"))
	fmt.Println(sub.NextNode(sub.FirstOut(node).Node()).Get("label"))
}
