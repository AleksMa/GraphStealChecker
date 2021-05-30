package check

import (
	"regexp"
	"strings"
)

const (
	ControlEdge EdgeType = iota
	DataEdge
)

const (
	Root NodeType = iota
	Call
	Control // if, switch, for, while...
	Branch  // then, else ...
	Declaration
	Assignment
	Increment
	Return
	Expression
	Jump
	Label
	SwitchCase // case or default
	Another
	Count
)

// Определение класса Node по Label
func GetNodeType(inputLabel string) NodeType {
	label := strings.ToLower(inputLabel)
	controlRe := regexp.MustCompile(`^.*((if)|(for)|(while)).*$`)
	branchRe := regexp.MustCompile(`^.*((then)|(else)|(loop)).*$`)
	incrementRe := regexp.MustCompile(`^(.*\+\+.*)|(.*--.*)|(.*\+=.*)|(.*-=.*)|(.*/=.*)|(.*\*=.*)$`)
	expressionRe := regexp.MustCompile(`^.*[+\-*/%^~].*$`)
	callRe := regexp.MustCompile(`^\w+\(.*\)$`)
	returnRe := regexp.MustCompile(`^.*return.*$`)
	assignRe := regexp.MustCompile(`^\w+\s*=\s*.*$`)
	switch {
	case controlRe.MatchString(label):
		return Control
	case branchRe.MatchString(label):
		return Branch
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
