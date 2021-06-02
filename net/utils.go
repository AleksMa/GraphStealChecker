package net

import (
	"io"
	"log"
	"net/http"
	"os"
	"strconv"
)

// This function returns the filename(to save in database) of the saved file
// or an error if it occurs
func FileUpload(r *http.Request, path string, key string) (string, error) {
	// ParseMultipartForm parses a request body as multipart/form-data
	r.ParseMultipartForm(32 << 20)

	file, handler, err := r.FormFile(key) // Retrieve the file from form data

	if err != nil {
		return "", err
	}
	defer file.Close() // Close the file when we finish

	// This is path which we want to store the file
	f, err := os.OpenFile(path+"/temp/"+handler.Filename, os.O_WRONLY|os.O_CREATE, 0666)

	if err != nil {
		return "", err
	}

	// Copy the file to the destination path
	io.Copy(f, file)

	return handler.Filename, nil
}

func ParseArgs(r *http.Request, path string) ([]string, int, float64, float64) {
	programs := make([]string, 2)
	for i, key := range []string{"p1", "p2"} {
		program, err := FileUpload(r, path, key)
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

	return programs, limit, subgraphSize, likelihood
}
