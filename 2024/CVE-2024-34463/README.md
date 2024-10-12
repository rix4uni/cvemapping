# CVE-2024-34463

**Affected Devices**: BPL Smart Weighing Scale PWS-01-BT (https://www.bplmedicaltechnologies.com/product-details/weighing-scales/personal-weighing-scale-pws-01bt/)

**Vulnerability**: Insufficient security in the Bluetooth communication between the digital weighing scale and the associated app (https://bpl-bewell.en.aptoide.com/app)


## Steps to run the exploit

**Install *libbluetooth-dev* if not installed already using this command:**

```sudo apt-get update && apt-get install libbluetooth-dev```

**Compile the BLE Scanner:**

```cc scanner.c -o scanner -l bluetooth```

**Run the exploit:**

```python3 run.py```
