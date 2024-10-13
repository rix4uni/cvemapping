#include <stdio.h>
#include <stdlib.h>
int main() {
	char in[512];
	char key_name[512];
	FILE *fp;
	char name[16] = "ggla";
	unsigned long long refconut;
	fp = fopen("/proc/keys", "r");
	if(!fp) {
		perror("fopen");
		return -1;
	}
	while (fgets(in, 1024, fp) != NULL ) {
		sscanf(in, "%*s%*s%*s%*s%*s%*s%*s%*s %[^:]", key_name);
		if (!strcmp(name,key_name)) {
			fclose(fp);
			sscanf(in, "%*s%*s %llu", refconut);
			printf("%llu", refconut);
			return 0;
		}
	}
	fclose(fp);
	return -1;
}
