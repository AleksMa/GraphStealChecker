package check

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"strconv"
	"strings"
)

func Check(path string, programs []string, subgraphSize float64, timeLimit int, likelihood float64) Result {
	var err error
	pathGraphs := path + "/temp/"

	nodesAll := make([][][]*Node, 2)
	files := make([][]CodeLine, 2)

	for i, program := range programs {
		file, err := os.Open(program)
		if err != nil {
			log.Fatal("preopen: ", err)
		}
		defer func() {
			if err = file.Close(); err != nil {
				log.Fatal(err)
			}
		}()

		b, err := ioutil.ReadAll(file)
		if err != nil {
			log.Fatal("prereading: ", err)
		}
		lines := strings.Split(string(b), "\n")
		for _, line := range lines {
			files[i] = append(files[i], CodeLine{
				Line:   line,
				Color:  "#000000",
				Parsed: true,
			})
		}
	}

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
		nodesAll[i], err = ParsePDG(pathDot, &(files[i]))
		if err != nil {
			log.Fatal("parser: ", err)
		}
	}

	for i, nodes := range nodesAll {
		graph := StringifyNodes(nodes)

		// open output file
		fo, err := os.Create(pathGraphs + fmt.Sprintf("graph%v.txt", i+1))
		if err != nil {
			log.Fatal("txt output: ", err)
		}
		// make a write buffer
		w := bufio.NewWriter(fo)
		_, err = w.Write([]byte(graph))
		if err != nil {
			log.Fatal("txt output: ", err)
		}

		err = w.Flush()
		if err != nil {
			log.Fatal("txt output: ", err)
		}
		// close fo on exit and check for its returned error
		if err := fo.Close(); err != nil {
			log.Fatal("txt output: ", err)
		}
	}

	b, err := exec.Command(
		path+"/PyMCS/run.py",
		path+"/temp/graph1.txt",
		path+"/temp/graph2.txt",
		fmt.Sprint(subgraphSize),
		fmt.Sprint(timeLimit),
		fmt.Sprint(likelihood)).
		Output()
	if err != nil {
		log.Fatal("mcis: ", err)
	}

	var nodeFunctionsComp []*NodeComp
	var funcsPlag []PlagFunc
	plagiarism := 0.0

	for _, line := range strings.Split(string(b), "\n") {
		elems := strings.Split(line, " ")
		if len(elems) == 4 {
			i1, _ := strconv.Atoi(elems[0])
			i2, _ := strconv.Atoi(elems[1])
			likely, _ := strconv.ParseFloat(elems[2], 64)
			nodeFunctionsComp = append(nodeFunctionsComp, ParseNodesComp(i1, i2, elems[3]))
			if likely >= 0.1 {
				fmt.Printf(
					"%s vs %s: %v\n",
					PrettifyFuncName(nodesAll[0][i1][0].Label),
					PrettifyFuncName(nodesAll[1][i2][0].Label),
					likely,
				)
				funcsPlag = append(funcsPlag, PlagFunc{
					FuncLeft:   PrettifyFuncName(nodesAll[0][i1][0].Label),
					FuncRight:  PrettifyFuncName(nodesAll[1][i2][0].Label),
					Plagiarism: likely,
				})
			}
		} else if len(elems) == 1 {
			plag, _ := strconv.ParseFloat(elems[0], 64)
			fmt.Println("Plagiarism:", plag)
			plagiarism = plag
			break
		}
	}

	for i, comp := range nodeFunctionsComp {
		linesComp1 := make(map[int]struct{}, len(comp.Comp))
		linesComp2 := make(map[int]struct{}, len(comp.Comp))
		for k, v := range comp.Comp {

			start, end := nodesAll[0][i][k].Start, nodesAll[0][i][k].End
			if start != -1 && end != -1 {
				for j := start; j <= end; j++ {
					linesComp1[j] = struct{}{}
					files[0][j-1].Color = "#b71c1c"
				}
			}
			start, end = nodesAll[1][comp.Function][v].Start, nodesAll[1][comp.Function][v].End
			if start != -1 && end != -1 {
				for j := start; j <= end; j++ {
					linesComp2[j] = struct{}{}
					files[1][j-1].Color = "#b71c1c"
				}
			}
		}
	}

	names := []string{
		programs[0],
		programs[1],
	}
	for i := range names {
		splitted := strings.Split(names[i], "/")
		if len(splitted) <= 1 {
			splitted = strings.Split(names[i], "\\")
			if len(splitted) <= 1 {
				continue
			}
		}
		names[i] = splitted[len(splitted)-1]
	}
	return Result{
		LinesLeft:  files[0],
		LinesRight: files[1],
		NameLeft:   names[0],
		NameRight:  names[1],
		Plagiarism: plagiarism,
		PlagFuncs:  funcsPlag,
	}
}
