#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>


int main(void)
{

	if (setuid(0) == 0)
		execlp("/bin/sh", "/bin/sh", NULL);


	printf("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF\n");
	return EXIT_FAILURE;

}
