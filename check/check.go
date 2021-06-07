package check

import (
	"bytes"
	"fmt"
	"log"
	"os/exec"
	"strconv"
	"strings"
	"time"
)

// Основная функция проверки программ на предмет совпадений

func Check(path string, programs []string, subgraphSize float64, timeLimit int, likelihood float64) Result {
	pathGraphs := path + "/temp/"

	codeLines := CreateCodeLines(programs)
	nodesAll := CreateNodesSet(path, programs, codeLines)

	WriteInnerGraph(pathGraphs, nodesAll)

	now := time.Now()

	cmd := exec.Command(
		path+"/PyMCS/run.py",
		path+"/temp/graph1.txt",
		path+"/temp/graph2.txt",
		fmt.Sprint(subgraphSize),
		fmt.Sprint(timeLimit),
		fmt.Sprint(likelihood))

	var b bytes.Buffer
	cmd.Stdout = &b

	cmd.Start()

	done := make(chan error)
	go func() { done <- cmd.Wait() }()

	timeout := time.After(time.Duration(timeLimit) * time.Second)

	select {
	case <-timeout:
		// Timeout happened first, kill the process and print a message.
		cmd.Process.Kill()
	case err := <-done:
		// Command completed before timeout. Print output and error if it exists.
		if err != nil {
			log.Fatal("mcis: ", err)
		}
	}

	nodeFunctionsComp := map[int]*NodeComp{}
	var funcsPlag []PlagiarisedFunc
	plagiarism := 0

	firstToSecond := map[int]CompWeight{}
	secondToFirst := map[int]int{}

	for _, line := range strings.Split(string(b.Bytes()), "\n") {
		elems := strings.Split(line, " ")
		if len(elems) == 4 {
			i1, _ := strconv.Atoi(elems[0])
			i2, _ := strconv.Atoi(elems[1])
			likely, _ := strconv.ParseFloat(elems[2], 64)
			nodeFunctionsComp[i1] = ParseNodesComp(i1, i2, elems[3])
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

				if i1prev, ok := secondToFirst[i2]; ok {
					if firstToSecond[i1prev].Weight < likely {
						delete(firstToSecond, i1prev)
					} else {
						continue
					}
				}

				firstToSecond[i1] = CompWeight{
					Function: i2,
					Weight:   likely,
				}
				secondToFirst[i2] = i1
			}
		} else if len(elems) == 1 {
			plag, _ := strconv.ParseFloat(elems[0], 64)
			plagiarism = int(plag * 100)
			break
		}
	}

	fmt.Println("Plagiarism: ", plagiarism)
	fmt.Println(int(time.Since(now).Seconds()))

	for i, comp := range nodeFunctionsComp {
		linesComp := make(map[int][]int, len(comp.Comp))
		first := true
		for k, v := range comp.Comp {
			start, end := nodesAll[0][i][k].Start, nodesAll[0][i][k].End
			if start != -1 && end != -1 {
				for j := start; j <= end; j++ {
					start2, end2 := nodesAll[1][comp.Function][v].Start, nodesAll[1][comp.Function][v].End
					if linesComp[j] == nil {
						linesComp[j] = make([]int, 0, end2-start2+1)
					}
					if start2 != -1 && end2 != -1 {
						for l := start2; l <= end2; l++ {
							linesComp[j] = append(linesComp[j], l)
							if first {
								if left, ok := firstToSecond[i]; ok && left.Function == comp.Function {
									codeLines[1][l-1].Color = "#b71c1c"
								}
							}
						}
					}
					if left, ok := firstToSecond[i]; ok && left.Function == comp.Function {
						codeLines[0][j-1].Color = "#b71c1c"
					}
					first = false
				}
			}
			first = true
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
