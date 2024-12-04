package main

import (
	"encoding/binary"
	"log"
	"net"

	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
)

func main() {
	// 1. Set up the target information
	srcdstIP := net.ParseIP("127.0.0.1")
	srcPort := uint16(12345)
	dstPort := uint16(4242)

	originalUdpLayer := &layers.UDP{
		SrcPort: layers.UDPPort(srcPort),
		DstPort: layers.UDPPort(dstPort),
		Length:  1449,
	}
	originalUdpLayer.SetNetworkLayerForChecksum(&layers.IPv4{
		SrcIP:    srcdstIP,
		DstIP:    srcdstIP,
		Protocol: layers.IPProtocolUDP,
	})
	originalIpLayer := &layers.IPv4{
		Version:  4,
		SrcIP:    srcdstIP,
		DstIP:    srcdstIP,
		Protocol: layers.IPProtocolUDP,
		TTL:      64,
	}

	// Set MTU to a value smaller than 1200 bytes
	mtu := uint16(1100)
	payload := make([]byte, 4)
	binary.BigEndian.PutUint16(payload[2:], mtu)

	originalBuffer := gopacket.NewSerializeBuffer()
	err := gopacket.SerializeLayers(originalBuffer, gopacket.SerializeOptions{}, originalUdpLayer)
	if err != nil {
		log.Fatal(err)
	}
	// ipLayer := &layers.IPv4{
	// 	Version:  4,
	// 	SrcIP:    srcdstIP,
	// 	DstIP:    srcdstIP,
	// 	Protocol: layers.IPProtocolICMPv4,
	// 	TTL:      64,
	// }
	icmpLayer := &layers.ICMPv4{
		TypeCode: layers.CreateICMPv4TypeCode(3, 4),
	}

	// icmpPayload := append(payload, originalBuffer.Bytes()[:8]...)

	buffer := gopacket.NewSerializeBuffer()
	opts := gopacket.SerializeOptions{
		ComputeChecksums: true,
		FixLengths:       true,
	}

	err = gopacket.SerializeLayers(buffer, opts, icmpLayer, originalIpLayer, originalUdpLayer)
	if err != nil {
		log.Fatal(err)
	}

	conn, err := net.ListenPacket("ip4:icmp", "0.0.0.0")
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	_, err = conn.WriteTo(buffer.Bytes(), &net.IPAddr{IP: srcdstIP})
	if err != nil {
		log.Fatal(err)
	}

	log.Println("ICMP Packet Too Large message sent successfully")
}
