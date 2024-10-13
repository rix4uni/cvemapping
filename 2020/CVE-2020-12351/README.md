# Linux: Heap-Based Type Confusion in L2CAP (CVE-2020-12351)
**Linux: Heap-Based Type Confusion in L2CAP** PoC (CVE-2020-12351) on BLE implementation

## Why did I modify the original PoC?
The original [PoC][Andy Nguyen, Google Security Research Team] is focused on sending a malicious l2cap packet via Bluetooth Classic. However, I had a requirement to test it against a peripheral that supports only Bluetooth Low Energy (BLE) communication and has adopted the entire BlueZ stack (both classic and LE)

L2CAP is a common protocol that resides in host stack to support both bluetooth classic and BLE implementations


## Prerequisite
Linux Machine with BLE Adapter. If the machine doesn't come with an inbuilt adapter, you can a get an external one

## Usage: 
```sh
1. Compile 
gcc -o CVE-2020-12351 CVE-2020-12351.c -lbluetooth 

2. Run
$./CVE-2020-12351 <BLE_Peripheral_MAC_Address>      //MAC Format: FF:FF:FF:FF:FF:FF

Packet capture:
hcidump -i <hci0> -w CVE-2020-12351.pcap
```

## Acknowledgements
- [Andy Nguyen, Google Security Research Team]


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen)
   [Andy Nguyen, Google Security Research Team]: <https://github.com/google/security-research/security/advisories/GHSA-h637-c88j-47wq>
   
