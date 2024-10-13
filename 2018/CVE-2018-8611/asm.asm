_TEXT SEGMENT

EXTERNDEF NtQueryInformationResourceManager:proc 
EXTERNDEF NtQueryInformationThread:proc 

PUBLIC  NtQueryInformationResourceManager
NtQueryInformationResourceManager PROC
    mov r10, rcx
    mov eax, 144h;   
    syscall
    ret
NtQueryInformationResourceManager ENDP

PUBLIC  NtQueryInformationThread
NtQueryInformationThread PROC
    mov r10, rcx
    mov eax, 25h;   
    syscall
    ret
NtQueryInformationThread ENDP

_TEXT ENDS
END