#include "utils.h"
#include <vector>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <iostream>
#include <Psapi.h>

std::wofstream logFile("exploit_log.txt", std::ios::app);

void* GetKernelBase() {
    std::vector<LPVOID> drivers(1024);
    DWORD cbNeeded;
    if (EnumDeviceDrivers(drivers.data(), sizeof(LPVOID) * drivers.size(), &cbNeeded) && cbNeeded < sizeof(LPVOID) * drivers.size()) {
        return drivers[0]; // ntoskrnl.exe is usually the first driver loaded
    }
    return nullptr;
}

uintptr_t GetKernelFunctionAddress(const char* functionName) {
    void* kernelBase = GetKernelBase();
    if (!kernelBase) return 0;

    HMODULE hNtoskrnl = LoadLibraryA("ntoskrnl.exe");
    if (!hNtoskrnl) return 0;

    FARPROC funcAddress = GetProcAddress(hNtoskrnl, functionName);
    if (!funcAddress) return 0;

    uintptr_t offset = reinterpret_cast<uintptr_t>(funcAddress) - reinterpret_cast<uintptr_t>(hNtoskrnl);
    return reinterpret_cast<uintptr_t>(kernelBase) + offset;
}

void Log(const std::wstring& message) {
    logFile << message << std::endl;
    logFile.flush();
    OutputDebugStringW(message.c_str());
    std::wcout << message << std::endl;
}

void LogPointer(const std::wstring& name, void* ptr) {
    std::wstringstream ss;
    ss << name << L": " << std::hex << std::setfill(L'0') << std::setw(16)
        << reinterpret_cast<uintptr_t>(ptr);
    Log(ss.str());
}