package main

import (
	"crypto/tls"
	"log"
	"net/http"
	"time"
)

func main() {
	c := &http.Client{
		Transport: &http.Transport{
			TLSClientConfig: &tls.Config{
				InsecureSkipVerify: false,
			},
		}}

	t := time.Now()
	if _, err := c.Get("https://l"); err != nil {
		log.Println(err)
	}
	log.Println(time.Since(t))
}
