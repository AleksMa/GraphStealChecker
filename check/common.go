package check

import "html/template"

// Общие структуры, используемые при проверке

// Отдельные типы для классов вершин и ребер графа зависимости программы
type NodeType int
type EdgeType int

// Итоговый результат проверки, отображаемый на веб-странице
type Result struct {
	LinesLeft  []CodeLine
	LinesRight []CodeLine
	NameLeft   string
	NameRight  string
	Plagiarism int
	PlagFuncs  []PlagiarisedFunc
}

// Структура, инкапсулирующая процент схожести для наиболее близких функций
type PlagiarisedFunc struct {
	FuncLeft   string
	FuncRight  string
	Plagiarism int
}

// Структура, инкапсулирующая строку кода
// Используется при отображении исходного текста на странице резальтатов
// Включает цвет текста для подсветки совпавших участков
type CodeLine struct {
	Line   template.HTML
	Color  string
	Parsed bool
}

// Структура, инкапсулирующая отображение (изоморфизм) совпавших подграфов
type NodeComp struct {
	Function int
	Comp     map[int]int
}

type CompWeight struct {
	Function int
	Weight   float64
}

// Внутреннее представление ребер графа зависимости программы
type Edge struct {
	Destination *Node
	Type        EdgeType
}

// Внутреннее представление вершин графа зависимости программы
type Node struct {
	Type   NodeType
	Number int
	Edges  []*Edge
	Label  string
	Name   string
	Start  int
	End    int
}
