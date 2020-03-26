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

type postVars struct {
	URL      string
	MaxNodes int64
	Dynamic  bool
}

func main() {
	fs := http.FileServer(http.Dir("public"))
	http.Handle("/public/", http.StripPrefix("/public/", fs))
	http.HandleFunc("/map", mmap)

	////
	// fs := http.FileServer(http.Dir("public"))
	// http.Handle("/", fs)
	////
	fmt.Println("Listening...")
	err := http.ListenAndServe(GetPort(), nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
		return
	}
}
func mmap(w http.ResponseWriter, req *http.Request) {
	if req.Method == http.MethodPost {
		fmt.Println("submission attempt...")

		postURL := req.FormValue("url")
		postMaxNodes := req.FormValue("maxnodes")
		postDynamic := req.FormValue("dynamic")
		// postMaxNodes, err := strconv.ParseInt(
		// 	req.FormValue("maxnodes"), 10, 64)
		// if err != nil {
		// 	log.Println(err)
		// }
		// postDynamic, err := strconv.ParseBool(
		// 	req.FormValue("dynamic"))
		// if err != nil {
		// 	log.Println(err)
		// }

		// pyvars := postVars{
		// 	URL:      postURL,
		// 	MaxNodes: postMaxNodes,
		// 	Dynamic:  postDynamic,
		// }

		// fmt.Println(pyvars)
		sendData(postURL, postMaxNodes, postDynamic)

	}
	// fmt.Fprintf(w, "map is this")
	http.ServeFile(w, req, "./public/map.html")
	fmt.Println("we are at map page")
}

// Gets the port from the environment
func GetPort() string {
	var port = os.Getenv("PORT")
	// Set a default port if there is nothing in the environment
	if port == "" {
		port = "5000"
		fmt.Println("INFO: No PORT environment variable detected, defaulting to " + port)
	}
	return ":" + port
}

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

func copyOutput(r io.Reader) {
	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		fmt.Println(scanner.Text())
	}
}
