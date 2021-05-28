package main

import (
	"flag"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/AleksMa/GraphStealChecker/check"
	"github.com/AleksMa/GraphStealChecker/net"
)

func ParseArgs() (port int) {
	portArg := flag.Int("p", 8181, "service port")
	flag.Parse()

	port = *portArg
	return
}

func main() {
	port := ParseArgs()
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

		var (
			limit        = 5
			subgraphSize = 0.7
			likelihood   = 0.99
			err          error
		)
		limitArg := r.FormValue("limit")
		if len(limitArg) != 0 {
			limit, err = strconv.Atoi(limitArg)
			if err != nil {
				log.Fatal("time limit parse:", err)
			}
		}

		subgraphArg := r.FormValue("subgraph")
		if len(subgraphArg) != 0 {
			subgraphSize, err = strconv.ParseFloat(subgraphArg, 64)
			if err != nil {
				log.Fatal("subgraph size parse:", err)
			}
		}

		likelihoodArg := r.FormValue("likelihood")
		if len(likelihoodArg) != 0 {
			likelihood, err = strconv.ParseFloat(likelihoodArg, 64)
			if err != nil {
				log.Fatal("time limit parse:", err)
			}
		}
		fmt.Println(subgraphSize, limit, likelihood)

		now := time.Now()

		files := check.Check(path, programs, subgraphSize, limit, likelihood)
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

	fmt.Printf("http://127.0.0.1:%v\n", port)
	err = http.ListenAndServe(fmt.Sprintf(":%v", port), nil)
	if err != nil {
		log.Fatal(err)
	}
}
