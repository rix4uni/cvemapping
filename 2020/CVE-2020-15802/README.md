# README


Repository about the BLUR attacks presented at AsiaCCS'22  in the paper titled: **BLURtooth: Exploiting
Cross-Transport Key Derivation in Bluetooth Classic and Bluetooth Low Energy.** 

Useful links:
[pdf](https://nebelwelt.net/files/22AsiaCCS.pdf),
[video](https://www.youtube.com/watch?v=FzFQD3XTLlA),
[slides](https://francozappa.github.io/publication/2022/blur/slides.pdf),
[website](https://hexhive.epfl.ch/BLURtooth/).


BibTex entry:

```
@inproceedings{antonioli22blur,
    author={Antonioli, Daniele and Tippenhauer, Nils Ole and Rasmussen, Kasper
    and Payer, Mathias},
    title={{BLURtooth: Exploiting Cross-Transport Key Derivation in
    Bluetooth Classic and Bluetooth Low Energy}},
    booktitle={Proceedings of the  Asia conference on computer and
    communications security (ASIACCS)},
    month={May},
    year={2022}
}

```


The BLUR attacks have been assigned 
[CVE-2020-15802](https://nvd.nist.gov/vuln/detail/CVE-2020-15802) and
[CVE-2022-20361](https://nvd.nist.gov/vuln/detail/CVE-2022-20361).



## Initialization

In the remaining of the README we indicate *Bluetooth Classic (aka BR/EDR)* as *BT*
*Bluetooth Low Energy* as *BLE*, and *Cross-Transport Key Derivation* as *CTKD*.
We also assume that the attack device and the victims support BT,BLE and CTKD.
This means that the devices support Bluetooth 4.2+ and BT/BLE Secure Connections.

The easiest way to perform the attacks is to use one device both as a victim
and attack device. For example, we recommend to use a Linux laptop as
victim/attack device and any other device as the other victim.

We are using a Linux machine running [bluez](https://github.com/bluez/bluez) 
and [bluez tools](https://github.com/bluez/bluez/tree/master/tools). We
rely on the `btmgmt` tool and might be helpful to skim its 
[source code](https://github.com/bluez/bluez/blob/master/tools/btmgmt.c). In
particular we use its `pair` sub-command as, among others, it allows to send arbitrary
pairing requests over BT/BLE while declaring arbitrary input-output
capabilities.

    Usage: pair [-c cap] [-t type] <remote address>

If you want to reproduce the exact attack scenario presented in our paper you must do some extra work.
Specifically you need to reproduce the setup presented in
[BIAS attack](https://github.com/francozappa/bias). Once your setup is ready
you should be able to use the development board as your BT/BLE Controller, and
the Linux laptop as a Host. Moreover, you should be able to sniff the link
layer packets from the Host (e.g., BT LMP traffic) and to dynamically patch
the firmware of the development board at runtime using 
[internalblue](https://github.com/seemoo-lab/internalblue).






## Perform the BLUR attacks

### Hardcode NoInputNoOutput Capabilities (w/o unsetting the MitM flag)

This step is optional and requires patching your own Linux kernel.

When using `btmgmt -c 3` bluez automatically unsets the MitM protection flag,
e.g., it sets the AuthReq byte to `0x02` other than `0x03`.
However, the BLUR attacks do not require to unset this flag but only require
to declare `NoInputNoOutput` capabilities when the remote device supports
input-output capabilities. Doing this trick the pairing procedure is
downgraded to Just Works *without* unsetting the MitM flag.

Implementing this setup requires a minimal modification of the Linux kernel. In
particular, in `/net/bluetooth/hci_event.c` we change:

    cp.authentication = conn->auth_type;

to:

    cp.authentication = 0x03;

Doing so, we hardcode our AuthReq flag to `0x03` regardless of the
input-output capabilities that we declare.

### Legitimate pairing

Pair the victim devices as usual. For example, if you are targeting a
smartphone pair it with your laptop (acting both as a victim and attack
device). Some user interaction might be required as part of pairing (e.g.,
Numeric Comparison).

### Open a btmgmt shell

* Take note of the victim Bluetooth address, indicated as `REMOTE-BTADD`
* Open a terminal
* Run `hciconfig` and take note of your hci index, .e.g, `0`
* Run `sudo btmgmt -i 0`
* You should see a blue terminal prompt containing `[hci0] #`


### Central Impersonation attack over BLE, [over]writing BT pairing key

Here I'm assuming that the victim is using a public BLE address. If it is using
a random one change the `-t` option to `2`

From the btmgmt CLI run:

    pair -t 1 REMOTE-BTADD

If you need also to downgrade association to Just Works run:

    pair -c 3 -t 1 REMOTE-BTADD

The `-c` flag set the input-output capabilities of the attacker and a value of
`0x3` maps to `NoInputNoOutput`, while the default value for a laptop/smartphone
is `0x1` mapping to `Display Yes/No`.


### Peripheral Impersonation attack over BT, [over]writing BLE pairing key

In this case even if we impersonate a BLE peripheral we pair over BT as the
Central.

From the btmgmt CLI run:

    pair -t 0 REMOTE-BTADD

If you need also to downgrade association to Just Works run:

    pair -c 3 -t 0 REMOTE-BTADD


### Unindented session attacks

Repeat the attacks described above while impersonating a device that is
currently unknown to (i.e., not paired with) the victim.


## Q&A (Bluetooth, CTKD, Linux, bluez, Wireshark)

### How do I set my BT/BLE device discoverable/connectable/pairable?

From the `bluetoothctl` CLI you can set
`discoverable` to `on` or `off` and `pairable`. From the `btmgmt` CLI you can
also set the `connectable` flag.

### How can I control for how long my device is discoverable?

From `bluetoothctl`,
you can control the discoverability timeout using `discoverable-timeout`,
e.g., if you set it to `0` the device is always discoverable.


### How can I check if my BT/BLE device support pairing or is pairable?

For BT, while pairing with a remote device either as a Central or a
Peripheral, you will receive the following LMP packet: *LMP not accepted ext* (opcode: `0x02`) with pairing 
not allowed (error code: `0x18`)

For BLE, while pairing with a remote device either as a Central or a
Peripheral, you will receive the following SMP packet: *SMP Pairing Failed Command*
(opcode `0x05`) with *Pairing Not Supported* (reason `0x05`).

### How can I check if my BT/BLE device support Secure Connections?

For BT, while pairing with a remote device look at Secure Connections support
for the Host and the Controller in the LMP feature packages, e.g., using the
following Wireshark display filter: `btbrlmp.efeat.scc or btbrlmp.efeat.sch`.

For BLE, while pairing with a remote device in the SMP Pairing Request or
Response check the AuthReq byte containing the Secure Connection flag, e.g.,
using the following Wireshark display filter: `btsmp.sc_flag == 1`.

### How can I check if my BT/BLE device support CTKD?

For BT, while pairing with a remote device the BLE SMP traffic is tunneled
over L2CAP. Hence by using the `btl2cap.payload` Wireshark filter you should see one
packet from the Central to the Peripheral containing a payload starting with
`0x01` (SMP Pairing Request) and another packet in the other direction with a
payload beginning with `0x02` (SMP Pairing Response). Then you should also see
other raw L2CAP packets encoding the SMP key distribution phase.

For BLE, while pairing with a remote device in the SMP Pairing Request or
Response check that both the Central and the Peripheral are willing to send
and receive a link key during SMP key distribution,  e.g., use the following Wireshark 
filter `btsmp.key_dist_linkkey or btsmp.key_dist_linkkey`.
