package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
)

// struct for variables that we submit from our form
type postVars struct {
	URL      string
	MaxNodes int64
	Dynamic  bool
}

func main() {
	// creates the file server for our website
	fs := http.FileServer(http.Dir("public"))
	// serves all files in the file server
	http.Handle("/public/", http.StripPrefix("/public/", fs))
	http.HandleFunc("/map", mmap)

	fmt.Println("Listening...")
	// serves the application on the designated port
	err := http.ListenAndServe(GetPort(), nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
		return
	}
}

// displays map.html, updates when user submits form
func mmap(w http.ResponseWriter, req *http.Request) {
	if req.Method == http.MethodPost {
		fmt.Println("submission attempt...")

		// collect values from form
		postURL := req.FormValue("url")
		postMaxNodes := req.FormValue("maxnodes")
		postDynamic := req.FormValue("dynamic")

		// send data to python script
		sendData(postURL, postMaxNodes, postDynamic)
	}
	http.ServeFile(w, req, "./public/map.html")
	fmt.Println("we are at map page")
}

// GetPort gets the port from the environment
func GetPort() string {
	var port = os.Getenv("PORT")
	// Set a default port if there is nothing in the environment
	if port == "" {
		port = "8080"
		fmt.Println("INFO: No PORT environment variable detected, defaulting to " + port)
	}
	return ":" + port
}

// sends data to python script
func sendData(url string, maxnodes string, dynamic string) {
	cmd := exec.Command("python3", "./arg.py", "--url", url, "--mn", maxnodes, "--dy", dynamic)

	stdout, err := cmd.StdoutPipe()
	if err != nil {
		panic(err)
	}
	stderr, err := cmd.StderrPipe()
	if err != nil {
		panic(err)
	}
	err = cmd.Start()
	if err != nil {
		panic(err)
	}

	go copyOutput(stdout)
	go copyOutput(stderr)
	cmd.Wait()
}

// collects printed output from python script
func copyOutput(r io.Reader) {
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		fmt.Println(scanner.Text())
	}
}
