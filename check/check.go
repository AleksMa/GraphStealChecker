package check

import (
	"fmt"
	"log"
	"os/exec"
	"strconv"
	"strings"
)

// Основная функция проверки программ на предмет совпадений

func Check(path string, programs []string, subgraphSize float64, timeLimit int, likelihood float64) Result {
	var err error
	pathGraphs := path + "/temp/"

	codeLines := CreateCodeLines(programs)
	nodesAll := CreateNodesSet(path, programs, codeLines)

	WriteInnerGraph(pathGraphs, nodesAll)

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
	var funcsPlag []PlagiarisedFunc
	plagiarism := 0

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
				funcsPlag = append(funcsPlag, PlagiarisedFunc{
					FuncLeft:   PrettifyFuncName(nodesAll[0][i1][0].Label),
					FuncRight:  PrettifyFuncName(nodesAll[1][i2][0].Label),
					Plagiarism: int(likely * 100),
				})
			}
		} else if len(elems) == 1 {
			plag, _ := strconv.ParseFloat(elems[0], 64)
			fmt.Println("Plagiarism:", plag)
			plagiarism = int(plag * 100)
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
					codeLines[0][j-1].Color = "#b71c1c"
				}
			}
			start, end = nodesAll[1][comp.Function][v].Start, nodesAll[1][comp.Function][v].End
			if start != -1 && end != -1 {
				for j := start; j <= end; j++ {
					linesComp2[j] = struct{}{}
					codeLines[1][j-1].Color = "#b71c1c"
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
		LinesLeft:  codeLines[0],
		LinesRight: codeLines[1],
		NameLeft:   names[0],
		NameRight:  names[1],
		Plagiarism: plagiarism,
		PlagFuncs:  funcsPlag,
	}
}
