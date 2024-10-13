# CVE-2017-10235: VirtualBox E1000 device buffer overflow

## Introduction

The following document details a bug found in VirtualBox v5.1.22 (now fixed in v5.1.24), in the guest device emulation component `DevE1000` (*Intel 82540EM Ethernet Controller Emulation*), in the function `e1kFallbackAddToFrame`, which leads to a buffer overflow in the host when the guest OS is controlled by an attacker.

The bug was acknowledged by Oracle in the [CPU of July 2017](http://www.oracle.com/technetwork/security-advisory/cpujul2017-3236622.html#AppendixOVIR) with the issued [CVE-2017-10235](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-10235).

The vulnerability was corroborated with both a Linux (Ubuntu 16.04) and a Windows (v8.1) host running a Linux (also Ubuntu 16.04) guest, but the vulnerability could be triggered in many different host/guest combinations. In all scenarios the default network configuration is assumed: only one network adapter **attached to NAT** of type **Intel PRO/1000 MT Desktop (82540EM)**.

Since control structures (including function pointers) can be overwritten with attacker controlled data, it is safe to assume that remote code execution could be achieved in many scenarios. Oracle assigned a low CVSS score to this bug because it regarded that it had a `None` confidentiality risk and a `Low` integrity, which we believe does not reflect the full compromising potentiality of this bug (an explanation for the possibility of RCE is given below).


## Bug description and exploitation

The VirtualBox code that implements the emulation of the [Intel 82540EM Ethernet Controller][intel_manual] (in [`src/VBox/Devices/Network/DevE1000.cpp`][DevE1000_cpp]), in the function [`e1kFallbackAddToFrame`][e1kFallbackAddToFrame], implements the hardware TCP Segmentation:

```c

static int e1kFallbackAddToFrame(PE1KSTATE pThis, E1KTXDESC *pDesc,
                                bool fOnWorkerThread)
{
#ifdef VBOX_STRICT
   PPDMSCATTERGATHER pTxSg = pThis->CTX_SUFF(pTxSg);
   Assert(e1kGetDescType(pDesc) == E1K_DTYP_DATA);
   Assert(pDesc->data.cmd.fTSE);
   Assert(!e1kXmitIsGsoBuf(pTxSg));
#endif

   uint16_t u16MaxPktLen = pThis->contextTSE.dw3.u8HDRLEN +
                           pThis->contextTSE.dw3.u16MSS;
   Assert(u16MaxPktLen != 0);
   Assert(u16MaxPktLen < E1K_MAX_TX_PKT_SIZE);
```

This function correctly checks that the max TX packet length (`u16MaxPktLen`) is below the standard maximum of 16288 bytes (`E1K_MAX_TX_PKT_SIZE`), but does it in the form of an `Assert` macro that will be disabled in a release build, effectively leaving the check useless for the end user. This can be contrasted to the analogous function [`e1kAddToFrame`][e1kAddToFrame], which enforces the check with an explicit `if` instead of the `Assert`:

```c

static bool e1kAddToFrame(PE1KSTATE pThis, RTGCPHYS PhysAddr,
                         uint32_t cbFragment)
{
   PPDMSCATTERGATHER   pTxSg    = pThis->CTX_SUFF(pTxSg);
   bool const          fGso     = e1kXmitIsGsoBuf(pTxSg);
   uint32_t const      cbNewPkt = cbFragment + pThis->u16TxPktLen;

   if (RT_UNLIKELY( !fGso && cbNewPkt > E1K_MAX_TX_PKT_SIZE ))
   {
       E1kLog(("%s Transmit packet is too large: %u > %u(max)\n",
               pThis->szPrf, cbNewPkt, E1K_MAX_TX_PKT_SIZE));
       return false;
   }
```

The difference between the use of the normal function (`e1kAddToFrame`) and the fallback (`e1kFallbackAddToFrame`) is decided in `e1kXmitDesc()` and  depends on two factors: that the TSE flag is enabled in the data/context descriptors (controlled by the OS using the guest machine) and that the GSO flag is disabled. The latter depends on many factors, and hence there are many ways to disable it, but the most convenient is to enable the loopback mode, which is configured through the Receive Control Register (in the `RCTL.LBM` bits), also controlled by the guest OS.

Enabling the loopback mode will make the function [`e1kXmitAllocBuf`][e1kXmitAllocBuf] use the `aTxPacketFallback` buffer (*Transmit packet buffer use for TSE fallback and loopback*) for the allocation of the PDM scatter/gather buffer, with the mentioned length of 16288 bytes (`E1K_MAX_TX_PKT_SIZE`), and to signal that GSO will be disabled (by setting a `NULL` in `pvUser`).

```c

if (RT_LIKELY(GET_BITS(RCTL, LBM) != RCTL_LBM_TCVR))
{

  ...

}
else
{
 /* Create a loopback using the fallback buffer and preallocated SG. */
 AssertCompileMemberSize(E1KSTATE, uTxFallback.Sg, 8 * sizeof(size_t));
 pSg = &pThis->uTxFallback.Sg;
 pSg->fFlags      = PDMSCATTERGATHER_FLAGS_MAGIC |
                    PDMSCATTERGATHER_FLAGS_OWNER_3;
 pSg->cbUsed      = 0;
 pSg->cbAvailable = 0;
 pSg->pvAllocator = pThis;
 pSg->pvUser      = NULL; /* No GSO here. */
 pSg->cSegs       = 1;
 pSg->aSegs[0].pvSeg = pThis->aTxPacketFallback;
 pSg->aSegs[0].cbSeg = sizeof(pThis->aTxPacketFallback);
}
```

This will cause the call to the function `e1kXmitIsGsoBuf` (inside [`e1kXmitDesc`][e1kXmitDesc]) to return `False` and, with the TSE enabled in the data descriptor, the execution flow will go to [`e1kFallbackAddToFrame`][e1kFallbackAddToFrame_call] (instead of the safer function `e1kAddToFrame` with the correct check).

```c

/*
 * Add the descriptor data to the frame.  If the frame is complete,
 * transmit it and reset the u16TxPktLen field.
 */
if (e1kXmitIsGsoBuf(pThis->CTX_SUFF(pTxSg)))
{

  ...

}
else if (!pDesc->data.cmd.fTSE)
{

  ...

}
else
{
    STAM_COUNTER_INC(&pThis->StatTxPathFallback);
    rc = e1kFallbackAddToFrame(pThis, pDesc, fOnWorkerThread);
}
```

Inside `e1kFallbackAddToFrame`, with the aforementioned check disabled in a release build, the MSS can be set arbitrarily large (up to 64K minus the HDRLEN), hence allowing an arbitrarily large `DTALEN` to be passed to [`e1kFallbackAddSegment`][e1kFallbackAddSegment_call]:

```c

/*
* Carve out segments.
*/
int rc;
do
{
 /* Calculate how many bytes we have left in this TCP segment */
 uint32_t cb = u16MaxPktLen - pThis->u16TxPktLen;
 if (cb > pDesc->data.cmd.u20DTALEN)
 {
     /* This descriptor fits completely into current segment */
     cb = pDesc->data.cmd.u20DTALEN;
     rc = e1kFallbackAddSegment(pThis, pDesc->data.u64BufAddr, cb,
                 pDesc->data.cmd.fEOP /*fSend*/, fOnWorkerThread);
```

The function [`e1kFallbackAddSegment`][e1kFallbackAddSegment] will use this value (now as argument `u16Len`) to copy from guest memory into the buffer `aTxPacketFallback` in host memory (through `PDMDevHlpPhysRead`) without further checks to this length, thus causing the buffer overflow (of a buffer capacity of 16288 bytes with a memory size of up to 64K).

```c

static int e1kFallbackAddSegment(PE1KSTATE pThis, RTGCPHYS PhysAddr,
                   uint16_t u16Len, bool fSend, bool fOnWorkerThread)
{
    int rc = VINF_SUCCESS;
    /* TCP header being transmitted */
    struct E1kTcpHeader *pTcpHdr = (struct E1kTcpHeader *)
            (pThis->aTxPacketFallback + pThis->contextTSE.tu.u8CSS);
    /* IP header being transmitted */
    struct E1kIpHeader *pIpHdr = (struct E1kIpHeader *)
            (pThis->aTxPacketFallback + pThis->contextTSE.ip.u8CSS);

    E1kLog3(("%s e1kFallbackAddSegment: Length=%x, remaining payload=%x,
             header=%x, send=%RTbool\n", pThis->szPrf, u16Len,
             pThis->u32PayRemain, pThis->u16HdrRemain, fSend));
    Assert(pThis->u32PayRemain + pThis->u16HdrRemain > 0);

    PDMDevHlpPhysRead(pThis->CTX_SUFF(pDevIns), PhysAddr,
                      pThis->aTxPacketFallback + pThis->u16TxPktLen, u16Len);
```


Possible RCE
------------

To make this vulnerability more predisposed to an RCE, it has to be noted that the variable just after the buffer is its index (`u16TxPktLen`), used to write on it (as an offset on the argument of `PDMDevHlpPhysRead`). Controlling this value with an initial buffer overflow (caused by a first data descriptor of length `E1K_MAX_TX_PKT_SIZE` + 2 bytes) would then allow to write (in a second call to `PDMDevHlpPhysRead` with a second data descriptor) any memory address up to 64K of distance from the buffer, without being necessary to overwrite all the memory in-between  (which would make the attack more complicated, trying to avoid a potential crash).

Close to the target buffer [`aTxPacketFallback`][aTxPacketFallback], some lines below and within the 64K range, the [`g_aE1kRegMap`][g_aE1kRegMap] structured is defined, which includes a vector of function pointers that implement reading and writing handlers (`pfnRead` and `pfnWrite`) which would be an ideal target for the second buffer overflow to facilitate an RCE.


Bug in `e1kXmitAllocBuf`
--------------------------

A (minor) complication in this attack vector is worth mentioning for completeness: there is what seems like a bug in the function [`e1kXmitAllocBuf`][e1kXmitAllocBuf], where in the case of being in loopback mode, [`cbTxAlloc`][cbTxAlloc] (*Number of bytes in next packet*) is not reseted to zero, as it is done in the normal case ( in the other branch of its `if`). This causes the thread to get stuck in the `while` loop of `e1kLocateTxPacket` (inside `e1kXmitPending`):

```c

while (e1kLocateTxPacket(pThis))
{
   fIncomplete = false;
   /* Found a complete packet, allocate it. */
   rc = e1kXmitAllocBuf(pThis, pThis->fGSO);
   /* If we're out of bandwidth we'll come back later. */
   if (RT_FAILURE(rc))
       goto out;
   /* Copy the packet to allocated buffer and send it. */
   rc = e1kXmitPacket(pThis, fOnWorkerThread);
   /* If we're out of bandwidth we'll come back later. */
   if (RT_FAILURE(rc))
       goto out;
}
```

This seems to happen because [`e1kLocateTxPacket`][e1kLocateTxPacket] prematurely returns with `True` in the case where `cbTxAlloc` is not zero, and doesn't reach the code that checks if `iTxDCurrent` is equal to  `nTxDFetched` (the usual case where all descriptors have been processed), which would normally make the function return `False`, effectively terminating the aforementioned loop.

```c

static bool e1kLocateTxPacket(PE1KSTATE pThis)
{
   LogFlow(("%s e1kLocateTxPacket: ENTER cbTxAlloc=%d\n",
            pThis->szPrf, pThis->cbTxAlloc));
   /* Check if we have located the packet already. */
   if (pThis->cbTxAlloc)
   {
       LogFlow(("%s e1kLocateTxPacket: RET true cbTxAlloc=%d\n",
                pThis->szPrf, pThis->cbTxAlloc));
       return true;
   }
```

This translates to the requirement that the first packet sent to the device (after setting the loopback mode) has to be the one that triggers the overflow, otherwise the VM will hang (ending with a DoS rather than an RCE).


## Proof of concept

Because the setup of the network device is far from trivial, and to avoid building a custom driver for it, the E1000 driver of a generic Linux kernel was modified to generate the descriptors (both context and data) that trigger the overflow. This modified kernel is available for [download][poc_download] from this repo. It has been tested in an Ubuntu 16.04 guest, causing a crash both in Linux and Windows hosts. A detailed description is available [here](./poc/).


## Possible solutions

The vulnerability was fixed in [Changeset 67974][Changeset_67974] (`bugref:8881`). The checks made as `Assert` in `e1kFallbackAddToFrame` were converted to explicit checks as `if` statements, that now remain active in a release build (similar to what was already done in `e1kAddToFrame`). Also `cbTxAlloc` is now set to zero in both branches (loopback mode and normal mode) in `e1kXmitAllocBuf`.

An additional (defensive) check suggested here, not implemented in the changeset, could be to place, in `e1kFallbackAddSegment` (and similarly in `e1kAddToFrame`), before the call to `PDMDevHlpPhysRead`, to explicitly check for potential overflow the buffer with guest memory (mainly that `u16TxPktLen` plus `u16Len` be less that the `aTxPacketFallback` buffer length).


[DevE1000_cpp]: https://www.virtualbox.org/browser/vbox/trunk/src/VBox/Devices/Network/DevE1000.cpp?rev=64966
[e1kFallbackAddToFrame]: https://www.virtualbox.org/browser/vbox/trunk/src/VBox/Devices/Network/DevE1000.cpp?rev=64966#L4351
[e1kAddToFrame]: https://www.virtualbox.org/browser/vbox/trunk/src/VBox/Devices/Network/DevE1000.cpp?rev=64966#L4419
[e1kXmitAllocBuf]: https://www.virtualbox.org/browser/vbox/trunk/src/VBox/Devices/Network/DevE1000.cpp?rev=64966#L3684
[e1kXmitDesc]: https://www.virtualbox.org/browser/vbox/trunk/src/VBox/Devices/Network/DevE1000.cpp?rev=64966#L4795
[e1kFallbackAddToFrame_call]: https://www.virtualbox.org/browser/vbox/trunk/src/VBox/Devices/Network/DevE1000.cpp?rev=64966#L4898
[e1kFallbackAddSegment_call]: https://www.virtualbox.org/browser/vbox/trunk/src/VBox/Devices/Network/DevE1000.cpp?rev=64966#L4364
[e1kFallbackAddSegment]: https://www.virtualbox.org/browser/vbox/trunk/src/VBox/Devices/Network/DevE1000.cpp?rev=64966#L4153
[aTxPacketFallback]: https://www.virtualbox.org/browser/vbox/trunk/src/VBox/Devices/Network/DevE1000.cpp?rev=64966#L1180
[g_aE1kRegMap]: https://www.virtualbox.org/browser/vbox/trunk/src/VBox/Devices/Network/DevE1000.cpp?rev=64966#L1363
[cbTxAlloc]: https://www.virtualbox.org/browser/vbox/trunk/src/VBox/Devices/Network/DevE1000.cpp?rev=64966#L1166
[e1kLocateTxPacket]: https://www.virtualbox.org/browser/vbox/trunk/src/VBox/Devices/Network/DevE1000.cpp?rev=64966#L4985
[poc_download]: https://github.com/fundacion-sadosky/vbox_cve_2017_10235/releases/download/v1.0/linux-image-4.8.0-vbox-e1k-buffer-overflow-poc_4.8.0-1_amd64.deb
[Changeset_67974]: https://www.virtualbox.org/changeset/67974/vbox/trunk/src/VBox/Devices/Network/DevE1000.cpp
[intel_manual]: https://www.intel.com/content/dam/doc/manual/pci-pci-x-family-gbe-controllers-software-dev-manual.pdf
