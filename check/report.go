package check

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"strconv"
	"strings"
)

func ParseNodesComp(i1, i2 int, comp string) *NodeComp {
	pairs := strings.Split(comp[1:len(comp)-1], ",")

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

func CreateCodeLines(programs []string) [][]CodeLine {
	codeLines := make([][]CodeLine, 2)

	for i, program := range programs {
		file, err := os.Open(program)
		if err != nil {
			log.Fatal("open file: ", err)
		}
		defer func() {
			if err = file.Close(); err != nil {
				log.Fatal(err)
			}
		}()

		b, err := ioutil.ReadAll(file)
		if err != nil {
			log.Fatal("reading file: ", err)
		}
		lines := strings.Split(string(b), "\n")
		for _, line := range lines {
			codeLines[i] = append(codeLines[i], CodeLine{
				Line:   template.HTML(strings.Replace(strings.Replace(line, "\n", "<br>", -1), " ", "&nbsp;", -1)),
				Color:  "#000000",
				Parsed: true,
			})
		}
	}
	return codeLines
}

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
