
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

#include <sys/mman.h>
#include <sys/stat.h>
#include <linux/unistd.h>

#include <linux/in.h>

#define PR_SET_VMA      0x53564d41
#define PR_SET_VMA_ANON_NAME        0
#define MMAP_NUM 1

int read_file(const char *path)
{
    int fd = 0;
    int cnt = 0;
    int ret = 0;
    char buf[0x1000] = { '\0' };

    fd = open(path, O_RDONLY);
    if (fd < 0)
    {
        printf("open %s failed: %s", path, strerror(errno));
        return -1;
    }

    cnt = read(fd, buf, 0x1000);
    if (cnt < 0)
    {
        printf("read %s, %d failed: %s", path, cnt, strerror(errno));
        return -1;
    }
    buf[cnt - 1] = '\0';
    printf("%s:\n%s\n", path, buf);

    close(fd);
    return 0;
}

int main(int argc, char const *argv[])
{
    int ret = 0;
    unsigned long addr[MMAP_NUM] = { 0l };
    int i = 0;
    int j = 0;
    char *dummp = NULL;
    unsigned long value = 0;

    for (i = 0; i < MMAP_NUM; ++i)
    {
        addr[i] = (unsigned long)mmap((void *)(0x100000 + i * 0x1000), 0x1000,
                                    PROT_READ | PROT_WRITE | PROT_EXEC,
                                    MAP_SHARED | MAP_ANONYMOUS, -1, 0);
        if (addr[i] == -1)
        {
            perror("map");
            exit(-1);
        }
        for (j = 0; j < 0x1000 / sizeof(unsigned long); ++j)
        {
            *(unsigned long *)(addr[i] + j * sizeof(unsigned long)) = j;
        }
        printf("mmap=%lx\n", addr[i]);
    }

    read_file("/proc/self/maps");
    errno = 0;
    ret = syscall(__NR_prctl, PR_SET_VMA, PR_SET_VMA_ANON_NAME, addr[0], 0x3000, "HuNg");
    printf("ret=%d, %s\n", ret, strerror(errno));
    read_file("/proc/self/maps");

    printf("%lx\n", *(unsigned long *)(addr[0] + 0x500));
    printf("%lx\n", *(unsigned long *)(addr[0] + 0x2000));
#if 0
    for (i = 0; i < MMAP_NUM; ++i)
    {
        printf("munmap %lx\n", addr[i]);
        munmap((void *)addr[i], 0x1000);
    }
#endif

    return 0;
}