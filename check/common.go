package check

type EdgeType int
type NodeType int

type OppositeCodes struct {
	FileLeft  []CodeLine
	FileRight []CodeLine
}

type CodeLine struct {
	Line  string
	Color string
}

type NodeComp struct {
	Function int
	Comp     map[int]int
}

type FuncsComp struct {
	FirstLines  map[int]struct{}
	SecondLines map[int]struct{}
}

type Edge struct {
	Destination *Node
	Type        EdgeType
}

type Node struct {
	Type   NodeType
	Number int
	Edges  []*Edge
	Label  string
	Name   string
	Start  int
	End    int
}
