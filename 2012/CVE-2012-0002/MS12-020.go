package rdp

import (
	"encoding/binary"
	"fmt"
	"net"
)

var connection_request = []byte{
	0x03, 0x00, // TPKT Header version 03, reserved 0
	0x00, 0x0b, // Length
	0x06,       // X.224 Data TPDU length
	0xe0,       // X.224 Type (Connection request)
	0x00, 0x00, // dst reference
	0x00, 0x00, // src reference
	0x00, // class and options
}

var connectInitial = []byte{
	0x03, 0x00, 0x00, 0x65, // TPKT Header
	0x02, 0xf0, 0x80, // Data TPDU, EOT
	0x7f, 0x65, 0x5b, // Connect-Initial
	0x04, 0x01, 0x01, // callingDomainSelector
	0x04, 0x01, 0x01, // callingDomainSelector
	0x01, 0x01, 0xff, // upwardFlag
	0x30, 0x19, // targetParams + size
	0x02, 0x01, 0x22, // maxChannelIds
	0x02, 0x01, 0x20, // maxUserIds
	0x02, 0x01, 0x00, // maxTokenIds
	0x02, 0x01, 0x01, // numPriorities
	0x02, 0x01, 0x00, // minThroughput
	0x02, 0x01, 0x01, // maxHeight
	0x02, 0x02, 0xff, 0xff, // maxMCSPDUSize
	0x02, 0x01, 0x02, // protocolVersion
	0x30, 0x18, // minParams + size
	0x02, 0x01, 0x01, // maxChannelIds
	0x02, 0x01, 0x01, // maxUserIds
	0x02, 0x01, 0x01, // maxTokenIds
	0x02, 0x01, 0x01, // numPriorities
	0x02, 0x01, 0x00, // minThroughput
	0x02, 0x01, 0x01, // maxHeight
	0x02, 0x01, 0xff, // maxMCSPDUSize
	0x02, 0x01, 0x02, // protocolVersion
	0x30, 0x19, // maxParams + size
	0x02, 0x01, 0xff, // maxChannelIds
	0x02, 0x01, 0xff, // maxUserIds
	0x02, 0x01, 0xff, // maxTokenIds
	0x02, 0x01, 0x01, // numPriorities
	0x02, 0x01, 0x00, // minThroughput
	0x02, 0x01, 0x01, // maxHeight
	0x02, 0x02, 0xff, 0xff, // maxMCSPDUSize
	0x02, 0x01, 0x02, // protocolVersion
	0x04, 0x00, // userData
}

var userRequest = []byte{
	0x03, 0x00, // header
	0x00, 0x08, // length
	0x02, 0xf0, 0x80, // X.224 Data TPDU (2 bytes: 0xf0 = Data TPDU, 0x80 = EOT, end of transmission)
	0x28, // PER encoded PDU contents
}

var channelRequest = []byte{
	0x03, 0x00, 0x00, 0x0c,
	0x02, 0xf0, 0x80, 0x38,
}

func checkRDPVuln(ip string, port int) bool {

	// rdp除了最早期的RDP标志位以外，其他的版本默认都会走tls，默认情况下，Windows自带的远程桌面服务里面自动生成的证书，名称对应的就是主机名
	//所以这里的dialTCP是会不行的，对于后期的机器

	// 建立 TCP 连接
	sock, err := net.DialTCP("tcp", nil, &net.TCPAddr{IP: net.ParseIP(ip), Port: port})
	if err != nil {
		fmt.Println("Failed to connect to the target:", err)
		return false
	}
	defer sock.Close()

	sock.Write(connection_request)
	res := make([]byte, 1024)
	_, err = sock.Read(res)
	if err != nil {
		fmt.Println(err)
		return false
	}

	sock.Write(connectInitial)

	// Send userRequest
	sock.Write(userRequest)

	_, err = sock.Read(res)
	if err != nil {
		fmt.Println(err)
		return false
	}
	user1 := binary.BigEndian.Uint16(res[9:11])
	//chan1 := user1 + 1001

	// Send second userRequest
	sock.Write(userRequest)
	_, err = sock.Read(res)
	if err != nil {
		fmt.Println(1)
		return false
	}
	user2 := binary.BigEndian.Uint16(res[9:11])
	chan2 := user2 + 1001

	// Send channel request one
	sock.Write(append(channelRequest, uint16ToBytes(user1, chan2)...))
	_, err = sock.Read(res)
	if err != nil {
		fmt.Println(2)
		return false
	}
	if res[7] == 0x3e && res[8] == 0x00 {
		// Send ChannelRequestTwo - prevent BSoD
		//sock.Write(append(channelRequest, uint16ToBytes(user2, chan2)...))
		return true
	} else {
		fmt.Println(3)
		return false
	}

}

func uint16ToBytes(nums ...uint16) []byte {
	b := make([]byte, len(nums)*2)
	for i, num := range nums {
		binary.BigEndian.PutUint16(b[i*2:], num)
	}
	return b
}
