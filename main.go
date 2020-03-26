package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

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
