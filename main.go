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

		if r.Method != http.MethodPost {
			http.Redirect(w, r, fmt.Sprintf("http://127.0.0.1:%v", port), http.StatusPermanentRedirect)
			return
		}

		programs, limit, subgraphSize, likelihood := net.ParseArgs(r, path)

		now := time.Now()

		result := check.Check(path, programs, subgraphSize, limit, likelihood)
		fmt.Printf("Working %v seconds\n", int(time.Since(now).Seconds()))

		tmpl, err := template.New("tmpl").Parse(net.CheckTemplate)
		if err != nil {
			log.Fatal(err)
		}
		err = tmpl.Execute(w, result)
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
