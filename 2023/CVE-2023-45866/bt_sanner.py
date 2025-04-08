import bluetooth

print("[*] Scanning for nearby Bluetooth devices...")
devices = bluetooth.discover_devices(duration=8, lookup_names=True)

if not devices:
    print("[-] No Bluetooth devices found.")
else:
    print(f"[+] Found {len(devices)} device(s):\n")
    for addr, name in devices:
        print(f"    {addr} - {name}")
