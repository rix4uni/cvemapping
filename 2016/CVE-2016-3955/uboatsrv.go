package uboatdemo

import (
	"log"
	"net"
)

const (
	USBIP_DEFAULT_PORT = 3240
)

type UboatServer struct {
	listener *net.TCPListener
}

func New() (*UboatServer, error) {
	// for demo purposes we listen on localhost and only use default port

	listener, err := net.ListenTCP("tcp", &net.TCPAddr{net.ParseIP("127.0.0.1"), USBIP_DEFAULT_PORT, ""})
	if err != nil {
		return nil, err
	}

	return &UboatServer{listener}, nil
}

func (srv *UboatServer) Close() error {
	return srv.listener.Close()
}

func (srv *UboatServer) Serve() error {
	for {
		conn, err := srv.listener.Accept()

		if err == nil {
			go handleConnection(conn)
		} else {
			log.Println(err)
		}
	}
}
