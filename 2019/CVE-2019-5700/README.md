# CVE-2019-5700

Unfortunately, I don't have a trendy and clever name for this vulnerability. This bug is fairly simple to exploit. I actually sat on it for quite a while until I realized this might affect more devices than I initially thought.

#### Scope:
This bug affects Nvidia Tegra t114-t210 SoCs that boot Android boot images, however there is one important distinction to make: 

t114 based devices are severely more affected because of their unified bootloader that also loads the TOS (TLK - Nvidia's secure monitor), which means the bootloader is already running in secure context... 

On t124+ devices, Nvidia now uses nvtboot as an early stage bootloader that loads TOS prior to the vulnerable bootloader executing, which loads and executes the kernel. This means we are running in non-secure context.

#### Write-up
Let's take a look at the Android boot image header (v1 - prior to Android 9):
```
struct boot_img_hdr
{
    uint8_t magic[BOOT_MAGIC_SIZE];
    uint32_t kernel_size;  /* size in bytes */
    uint32_t kernel_addr;  /* physical load addr */

    uint32_t ramdisk_size; /* size in bytes */
    uint32_t ramdisk_addr; /* physical load addr */

    uint32_t second_size;  /* size in bytes */
    uint32_t second_addr;  /* physical load addr */

    uint32_t tags_addr;    /* physical addr for kernel tags */
    uint32_t page_size;    /* flash page size we assume */
    uint32_t unused;
    uint32_t os_version;
    uint8_t name[BOOT_NAME_SIZE]; /* asciiz product name */
    uint8_t cmdline[BOOT_ARGS_SIZE];
    uint32_t id[8]; /* timestamp / checksum / sha1 / etc */
    uint8_t extra_cmdline[BOOT_EXTRA_ARGS_SIZE];
};
```
We see the fields for some familiar images: kernel, ramdisk:

```
    uint32_t kernel_size;  /* size in bytes */
    uint32_t kernel_addr;  /* physical load addr */

    uint32_t ramdisk_size; /* size in bytes */
    uint32_t ramdisk_addr; /* physical load addr */
```

and sometimes tags (which is often used for device tree or ATAGS)

```
uint32_t tags_addr;    /* physical addr for kernel tags */
uint32_t page_size;    /* flash page size we assume */
```

What about the 'second' fields?

```
uint32_t second_size;  /* size in bytes */
uint32_t second_addr;  /* physical load addr */
```

While I've never seen it used on a production device personally, it is my understanding the 'second' image can be used for a second stage bootloader or an additional image that needs to be loaded. In my experience from research, most bootloaders from other OEMs will ignore this field - as it's not used - or they will apply sanity checks on the size and address.

Nvidia's bootloader DOES apply sanity checks to the kernel, ramdisk, and dtb - all of which have hardcoded loading addresses which means the loading addresses in the header are ignored. However, it looks like Nvidia perhaps forgot about this mostly forgotten image... while arbitrarily loading it without any sanity checks on the address or size. That's right - you can arbitrarily load any image, of any size, to any memory address accessible (everything on t114, non-secure memory on t124+). 

This means we can freely patch the bootloader in memory to suit our needs. Whether we want to skip signature verifcation (which comes immediately after loading all the images), hijack loading the TOS on t114 to get secure context code execution, or simply load some shellcode to dump sensitive information.

#### Exploitation:
Exploitation is as simple as creating a boot image with the secondary image as your payload/shellcode and the addr/len fields appropriately set to the size of your payload and where you want it to go. The image can be as small as 4-bytes.

#### Some important notes:
t124+ devices we do not have secure context, as nvtboot has already loaded the TOS in an earlier stage of booting which then hands off execution to a later stage bootloader (EBT), but we can still freely write to this late stage bootloader in memory. The vulnerable bootloader is the one that loads the kernel, so it is still rather valuable if you want to execute arbitrary unsigned code.

Not only is the loading address not verified, neither is the size, which opens the door to CVE-2019-5699 since we can overflow various variables/pointers by crafting a malicious secondary_size field. I cannot take credit for this though as I only realized it in hindsight after the initial security bulletin was published. It also seems like a lot more work...

#### Bootflow:
t114:

IROM->BCT->EBT->TOS->KERNEL

t124+ (may be slightly different for newer 64-bit SoC):

IROM->BCT->NVTBOOT->TOS->EBT->KERNEL

#### Timeline:
This issue was initially reported on July 29th, 2019 to Nvidia's PSIRT (Product Security Incident Response Team). They politely requested that I delay disclosure until all relevant customers had been notified and fixes rolled out - which I have happily complied with. They maintained communication throughout the process and were pleasant to work with. Today (December 5, 2019) Nvidia has finally finished releasing the fix to affected code and have posted two different security bulletins reflecting this issue, along with giving me the thumbs up for disclosure.

#### References:
https://nvidia.custhelp.com/app/answers/detail/a_id/4875

https://nvidia.custhelp.com/app/answers/detail/a_id/4910

#### Shoutouts:
balika011

beaups

npjohnson

djrbliss/Dan Rosenberg for making me meticulously check how bootloaders parse boot image headers
