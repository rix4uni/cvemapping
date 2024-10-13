package tcp

import (
	"bytes"
	"encoding/binary"
	"log"
	"strconv"
	"strings"
)

const (
	FIN = 1
	SYN = 2
	RST = 4
	PSH = 8
	ACK = 16
	URG = 32
)

type Header struct {
	Source      uint16
	Destination uint16
	SeqNum      uint32
	AckNum      uint32
	DataOffset  uint8
	Reserved    uint8
	ECN         uint8
	Ctrl        uint8
	Window      uint16
	Checksum    uint16
	Urgent      uint16
	Options     []Option
}

type Option struct {
	Kind   uint8
	Length uint8
	Data   []byte
}

func NewHeader(b []byte) *Header {
	var tcp Header
	r := bytes.NewReader(b)
	binary.Read(r, binary.BigEndian, &tcp.Source)
	binary.Read(r, binary.BigEndian, &tcp.Destination)
	binary.Read(r, binary.BigEndian, &tcp.SeqNum)
	binary.Read(r, binary.BigEndian, &tcp.AckNum)

	var mix uint16
	binary.Read(r, binary.BigEndian, &mix)
	tcp.DataOffset = byte(mix >> 12)
	tcp.Reserved = byte(mix >> 9 & 7)
	tcp.ECN = byte(mix >> 6 & 7)
	tcp.Ctrl = byte(mix & 0x3f)

	binary.Read(r, binary.BigEndian, &tcp.Window)
	binary.Read(r, binary.BigEndian, &tcp.Checksum)
	binary.Read(r, binary.BigEndian, &tcp.Urgent)

	return &tcp
}

func (tcp *Header) Marshal() []byte {
	buf := &bytes.Buffer{}
	binary.Write(buf, binary.BigEndian, tcp.Source)
	binary.Write(buf, binary.BigEndian, tcp.Destination)
	binary.Write(buf, binary.BigEndian, tcp.SeqNum)
	binary.Write(buf, binary.BigEndian, tcp.AckNum)

	var mix uint16
	mix = uint16(tcp.DataOffset)<<12 |
		uint16(tcp.Reserved)<<9 |
		uint16(tcp.ECN)<<6 |
		uint16(tcp.Ctrl)
	binary.Write(buf, binary.BigEndian, mix)

	binary.Write(buf, binary.BigEndian, tcp.Window)
	binary.Write(buf, binary.BigEndian, tcp.Checksum)
	binary.Write(buf, binary.BigEndian, tcp.Urgent)

	for _, option := range tcp.Options {
		binary.Write(buf, binary.BigEndian, option.Kind)
		if option.Length > 1 {
			binary.Write(buf, binary.BigEndian, option.Length)
			binary.Write(buf, binary.BigEndian, option.Data)
		}
	}
	out := buf.Bytes()

	// pad to min tcp header size
	pad := 20 - len(out)
	for i := 0; i < pad; i++ {
		out = append(out, 0)
	}
	return out
}

func (tcp *Header) HasFlag(flag byte) bool {
	return tcp.Ctrl&flag != 0
}

func to4Byte(ip string) [4]byte {
	parts := strings.Split(ip, ".")
	b0, err := strconv.Atoi(parts[0])
	if err != nil {
		log.Fatalf("Sockstress only works with ipv4 addresses.")
	}
	b1, _ := strconv.Atoi(parts[1])
	b2, _ := strconv.Atoi(parts[2])
	b3, _ := strconv.Atoi(parts[3])
	return [4]byte{byte(b0), byte(b1), byte(b2), byte(b3)}
}

// Source: https://en.wikipedia.org/wiki/Transmission_Control_Protocol#Checksum_computation
func Checksum(data []byte, srcip, dstip string) uint16 {
	srcIP := to4Byte(srcip)
	dstIP := to4Byte(dstip)

	pseudoHeader := []byte{
		srcIP[0], srcIP[1], srcIP[2], srcIP[3],
		dstIP[0], dstIP[1], dstIP[2], dstIP[3],
		0,
		6,
		0,
		byte(len(data)),
	}

	sumThis := make([]byte, 0, len(pseudoHeader)+len(data))
	sumThis = append(sumThis, pseudoHeader...)
	sumThis = append(sumThis, data...)

	lenSumThis := len(sumThis)
	var nextWord uint16
	var sum uint32
	for i := 0; i+1 < lenSumThis; i += 2 {
		nextWord = uint16(sumThis[i])<<8 | uint16(sumThis[i+1])
		sum += uint32(nextWord)
	}
	if lenSumThis%2 != 0 {
		//fmt.Println("Odd byte")
		sum += uint32(sumThis[len(sumThis)-1])
	}

	// Add back any carry, and any carry from adding the carry
	sum = (sum >> 16) + (sum & 0xffff)
	sum = sum + (sum >> 16)

	// Bitwise complement
	return uint16(^sum)
}
