package check

import (
	"regexp"
	"strings"
)

// Типы ребер
const (
	ControlEdge EdgeType = iota // Ребро зависимости управления
	DataEdge                    // Ребро зависимости данных
)

const (
	Root NodeType = iota
	Call
	Control // if, switch
	Branch  // then, else, case ...
	Cycle   // for, while...
	Declaration
	Assignment
	Increment
	Return
	Expression
	Jump // break, continue, goto, exit
	Another
	Count
)

// Определение класса Node по Label
func GetNodeType(inputLabel string) NodeType {
	label := strings.ToLower(inputLabel)
	controlRe := regexp.MustCompile(`^.*((if)|(switch)).*$`)
	cycleRe := regexp.MustCompile(`^.*((for)|(while)).*$`)
	branchRe := regexp.MustCompile(`^.*((then)|(else)|(loop)).*$`)
	jumpRe := regexp.MustCompile(`^.*((break)|(continue)|(goto)|(exit)).*$`)
	incrementRe := regexp.MustCompile(`^(.*\+\+.*)|(.*--.*)|(.*\+=.*)|(.*-=.*)|(.*/=.*)|(.*\*=.*)$`)
	expressionRe := regexp.MustCompile(`^.*[+\-*/%^~].*$`)
	callRe := regexp.MustCompile(`^\w+\(.*\)$`)
	returnRe := regexp.MustCompile(`^.*return.*$`)
	assignRe := regexp.MustCompile(`^\w+\s*=\s*.*$`)
	switch {
	case controlRe.MatchString(label):
		return Control
	case cycleRe.MatchString(label):
		return Cycle
	case branchRe.MatchString(label):
		return Branch
	case jumpRe.MatchString(label):
		return Jump
	case incrementRe.MatchString(label):
		return Increment
	case expressionRe.MatchString(label):
		return Expression
	case callRe.MatchString(label):
		return Call
	case returnRe.MatchString(label):
		return Return
	case assignRe.MatchString(label):
		return Assignment
	default:
		return Another
	}
}
