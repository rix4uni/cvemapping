.PHONY: all clean

CC=gcc
CFLAGS=

NASM=nasm
NASM_FLAGS=-f elf64

LD=ld


all: exploit crash

exploit: exploit.c
	$(CC) -o $@ $< $(CFLAGS)
	chmod +x $@

crash: crash.o
	$(LD) $^ -o $@
	strip crash


crash.o: crash.asm
	$(NASM) $(NASM_FLAGS) $^ 



clean:
	rm exploit crash *.o
