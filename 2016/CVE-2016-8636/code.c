#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<limits.h>
/*
int mem_check_range(struct rxe_mem *mem, u64 iova, size_t length)
{
  switch (mem->type) {
  // EI: no checks on the DMA regions - used only for local write... [22/10/2016]
  case RXE_MEM_TYPE_DMA:
    return 0;
  case RXE_MEM_TYPE_MR:
  case RXE_MEM_TYPE_FMR:
    // EI [FIX]: should fix this check to be:
    // EI      : ((iova   < mem->iova)   ||
    // EI      :  (length > mem->length) ||
    // EI      :  (iova   > (mem->iova + mem->length - length))) [22/10/2016]
    return ((iova < mem->iova) ||
           ((iova + length) > (mem->iova + mem->length))) ?
           -EFAULT : 0;

  default:
    return -EFAULT;
  }
}
*/

// possible replication


int  EFAULT = 5;
char RXE_MEM_TYPE_DMA = 'A';
char RXE_MEM_TYPE_MR = 'B';
char RXE_MEM_TYPE_FMR = 'C';

int mem_check_range(char mem_type, unsigned int iova, size_t length, int mem_iova, int mem_length)
{
	printf("mem_type = %c\n", mem_type);
	switch(mem_type) {

	case 'A':
		return 0;
	case 'B':
	case 'C':
		return ((iova < mem_iova) || ((iova + length) > (mem_iova + mem_length)))? -EFAULT:0;
	default:
		return 10;

	}
}

int main(int argc, char **argv)
{
	int value=10;
	unsigned int len = 5;
	int iova = 1000;
	int mem_length = 1000;
	int mem_iova = 1000;

	printf("Argv1 = %s\n", argv[1]);
	if(!strcmp(argv[1], "UINT_MAX"))
		{len = UINT_MAX;}
	else
		{len = 1200;}
	
	printf("So this is how the program might run\n");
	printf("Value of iova + len = %d\n", iova+len);
	value = mem_check_range(RXE_MEM_TYPE_MR, iova, len, mem_iova, mem_length);
	printf("value = %d\n", value);
	return 0;
}

