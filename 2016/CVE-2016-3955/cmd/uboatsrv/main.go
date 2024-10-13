package main

import (
	"log"

	demo "github.com/pqsec/uboatdemo"
)

func main() {
	srv, err := demo.New()
	if err != nil {
		log.Fatalln(err)
	}

	defer srv.Close()
	srv.Serve()
}
