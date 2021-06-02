package check

import (
	"html/template"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"
)

// Парсер изоморфизма общих подграфов пары функций i1 и i2, где i1 и i2 - номера функций первой и второй программы соответственно
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

// Конструктор "строк кода" с подцветкой (по умолчанию черный цвет для всех строк)
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
