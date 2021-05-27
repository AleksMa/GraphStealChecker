package net

import (
	"io"
	"net/http"
	"os"
)

// This function returns the filename(to save in database) of the saved file
// or an error if it occurs
func FileUpload(r *http.Request, key string) (string, error) {
	// ParseMultipartForm parses a request body as multipart/form-data
	r.ParseMultipartForm(32 << 20)

	file, handler, err := r.FormFile(key) // Retrieve the file from form data

	if err != nil {
		return "", err
	}
	defer file.Close() // Close the file when we finish

	// This is path which we want to store the file
	f, err := os.OpenFile(Path+"/temp/"+handler.Filename, os.O_WRONLY|os.O_CREATE, 0666)

	if err != nil {
		return "", err
	}

	// Copy the file to the destination path
	io.Copy(f, file)

	return handler.Filename, nil
}
