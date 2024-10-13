# Proof of Concept for the E1000 buffer overflow

This PoC uses a modified version of the Linux kernel to trigger, from the guest, a buffer overflow in the host. It usually just causes a crash in the host, resulting in a DoS, but this is just for simplicity, a more elaborate attack could be crafted that could lead to an RCE. This PoC was tested on an Ubuntu 16.04 guest to trigger the overflow. This modified kernel is available for [download][poc_download] from this repo.

[poc_download]: https://github.com/fundacion-sadosky/vbox_cve_2017_10235/releases/download/v1.0/linux-image-4.8.0-vbox-e1k-buffer-overflow-poc_4.8.0-1_amd64.deb

To verify the PoC install the kernel package inside the guest:

```bash

sudo dpkg -i linux-image-4.8.0-vbox-e1k-buffer-overflow-poc_4.8.0-1_amd64.deb
sudo reboot
```

The Linux kernel v4.8.0 (closest version to the current Ubuntu 16.04 kernel) was used, and its *Intel PRO/1000 Linux driver* (``drivers/net/ethernet/intel/e1000/e1000_main.c``) was modified to generate the transmit descriptors with the required characteristics to trigger the bug. An arbitrary value was chosen for the overflow length, of 50.000 bytes (has to be lower than 64K), to ensure a crash :

```
Context Descriptor:
	* MSS: 50.000
	* PAYLEN: 50.000
	* TUCMD.TSE: 1 (TCP Segmentation Enabled)
Data Descriptor:
	* DTALEN: 50.000
	* DCMD.TSE: 1
```

Both TSE flags have to be enabled (in the context and data descriptors) because different parts of the VBox code evaluate one or the other according to the context.

This corrupted descriptors are not injected (as they should be) in the TX ring, but rather (to simplify the code) normal descriptors sent by the OS to the driver are modified with the previous values. This means that it is up to the guest OS when the bug is triggered, but during normal operation (for common Linux distributions) that happens short after boot time.

Also, because of the potential bug in the loopback mode (described in the report), legacy descriptors (which are normally the first ones being sent by the OS) are discarded, as the loopback mode is enabled from the beginning in ``e1000_setup_rctl()`` (and not just before sending the corrupted descriptors), so the first packet sent to the emulation software has to be the one causing the overflow (after that, an infinite loop is entered and subsequent descriptors are not processed).

The modification to the driver (except for informative ``printk()`` calls) are enclosed in ``#ifdef`` clauses that evaluate the definition of the preprocessor constant ``VBOX_BUFFER_OVERFLOW_POC``, for conveniently disabling it and resuming normal operation (by commenting the corresponding ``#define``). These modifications are included in a [patch](./0001-e1k-buffer-overflow-poc.patch) that can be applied with the following code:

```bash

git clone git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git
cd linux-stable
git checkout -b e1k-buffer-overflow-poc v4.8
git apply ../0001-e1k-buffer-overflow-poc.patch
```
