#include <stdio.h>

int main(void)
{
    volatile int *p = NULL;
    *p = 42;
    return 0;
}
