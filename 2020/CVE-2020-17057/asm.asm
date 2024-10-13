_TEXT SEGMENT

EXTERNDEF NtDCompositionCreateChannel:proc 
EXTERNDEF NtDCompositionProcessChannelBatchBuffer:proc 

PUBLIC  NtDCompositionCreateChannel
NtDCompositionCreateChannel PROC
    mov r10, rcx
    mov eax, 1124h;   
    syscall
    ret
NtDCompositionCreateChannel ENDP

PUBLIC  NtDCompositionProcessChannelBatchBuffer
NtDCompositionProcessChannelBatchBuffer PROC
    mov r10, rcx
    mov eax, 1137h;
    syscall
    ret
NtDCompositionProcessChannelBatchBuffer ENDP

_TEXT ENDS
END