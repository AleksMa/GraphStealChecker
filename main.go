package main

import (
	"flag"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/AleksMa/GraphStealChecker/check"
	"github.com/AleksMa/GraphStealChecker/net"
)

var (
	SubgraphSize float64
	Likelihood   float64
	TimeLimit    int

	//NodeFunctionsComp []*NodeComp
	//LineFunctionsComp []*FuncsComp
	//
	//Files [][]CodeLine = make([][]CodeLine, 2)
)

func ParseArgs() {
	subgraphSize := flag.Float64("s", 0.9, "minimum common subgraph size")
	timeLimit := flag.Int("t", 10, "time limit on subgraph isomorphism")
	likelihoodLevel := flag.Float64("l", 0.995, "level of likelihood")
	flag.Parse()

	TimeLimit = *timeLimit
	SubgraphSize = *subgraphSize
	Likelihood = *likelihoodLevel
}

func main() {
	ParseArgs()
	path, err := os.Getwd()

	http.HandleFunc("/check", func(w http.ResponseWriter, r *http.Request) {

		programs := make([]string, 2)
		for i, key := range []string{"p1", "p2"} {
			program, err := net.FileUpload(r, path, key)
			if err != nil {
				log.Fatal("file upload: ", err)
			}
			programs[i] = path + "/temp/" + program
		}

		now := time.Now()

		files := check.Check(path, programs, SubgraphSize, TimeLimit, Likelihood)
		fmt.Printf("Working %v seconds\n", int(time.Since(now).Seconds()))

		tmpl, err := template.New("tmpl").Parse(net.CheckTemplate)
		if err != nil {
			log.Fatal(err)
		}
		err = tmpl.Execute(w, check.OppositeCodes{
			FileLeft:  files[0],
			FileRight: files[1],
		})
		if err != nil {
			log.Fatal(err)
		}
	})

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		tmpl, err := template.New("start").Parse(net.StartTemplate)
		if err != nil {
			log.Fatal(err)
		}
		err = tmpl.Execute(w, nil)
		if err != nil {
			log.Fatal(err)
		}
	})

	fmt.Println("http://127.0.0.1:8181")
	err = http.ListenAndServe(":8181", nil)
	if err != nil {
		log.Fatal(err)
	}
}
