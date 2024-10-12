# android-gadget

## Summary

Certain revisions of the Linux kernel used in Android are affected by issue [CVE-2021-39685](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-39685).
Detailed information and a POC for CVE-2021-39685 may be found in the [inspector-gadget](https://github.com/szymonh/inspector-gadget) repository. 

This repository includes POC targeting few Android specific USB gadgets including:
- f_accessory
- f_audio_source
- f_gsi
- f_mtp
- f_qc_rndis
- f_rmnet

## Description

a) f_accessory

- EP0 buffer allocated in composite.c is USB_COMP_EP0_BUFSIZ (4096) bytes large
- function's control tranfser handler acc_ctrlrequest reads ctrl->wLength to w_length
- for bRequest ACCESSORY_SEND_STRING or ACCESSORY_SEND_HID_EVENT value is set to w_length
- data transfer phase length is set to cdev->req->length = value;
- data transfer results in buffer overflow by wLength - 4096 bytes
- amount of data written to and past EP0 buffer is controller by attacker

```
int acc_ctrlrequest(struct usb_composite_dev *cdev,
				const struct usb_ctrlrequest *ctrl)
{
	struct acc_dev	*dev = get_acc_dev();
	int	value = -EOPNOTSUPP;
	struct acc_hid_dev *hid;
	int offset;
	u8 b_requestType = ctrl->bRequestType;
	u8 b_request = ctrl->bRequest;
	u16	w_index = le16_to_cpu(ctrl->wIndex);
	u16	w_value = le16_to_cpu(ctrl->wValue);
	u16	w_length = le16_to_cpu(ctrl->wLength);
	unsigned long flags;
    ...
	if (b_requestType == (USB_DIR_OUT | USB_TYPE_VENDOR)) {
        ...
        } else if (b_request == ACCESSORY_SEND_STRING) {
			dev_info(&cdev->gadget->dev, "%s: got ACCESSORY_SEND_STRING(52) request\n",
				__func__);
			schedule_work(&dev->sendstring_work);
			dev->string_index = w_index;
			cdev->gadget->ep0->driver_data = dev;
			cdev->req->complete = acc_complete_set_string;
			value = w_length;
            ...
		} else if (b_request == ACCESSORY_SEND_HID_EVENT) {
			spin_lock_irqsave(&dev->lock, flags);
			hid = acc_hid_get(&dev->hid_list, w_value);
			spin_unlock_irqrestore(&dev->lock, flags);
			if (!hid) {
				value = -EINVAL;
				goto err;
			}
			cdev->req->context = hid;
			cdev->req->complete = acc_complete_send_hid_event;
			value = w_length;
		}
...
	if (value >= 0) {
		cdev->req->zero = 0;
		cdev->req->length = value;
		value = usb_ep_queue(cdev->gadget->ep0, cdev->req, GFP_ATOMIC);
		if (value < 0)
			ERROR(cdev, "%s setup response queue error\n",
				__func__);
	}
```


b) f_audio_source

- EP0 buffer allocated in composite.c is USB_COMP_EP0_BUFSIZ (4096) bytes large
- function's control tranfser handler audio_setup reads ctrl->wLength to w_length
- for bRequestType matching condition USB_DIR_OUT | USB_TYPE_CLASS | USB_RECIP_ENDPOINT value variable is assigned to the return value of audio_set_endpoint_req
- audio_set_endpoint_req returns wLength for bRequest equal to UAC_SET_CUR, UAC_SET_MIN, UAC_SET_MAX or UAC_SET_RES
- data transfer phase length is set to value; req->length = value;
- data transfer results in buffer overflow by wLength - 4096 bytes
- amount of data written to and past EP0 buffer is controller by attacker

```
static int
audio_setup(struct usb_function *f, const struct usb_ctrlrequest *ctrl)
{
	struct usb_composite_dev *cdev = f->config->cdev;
	struct usb_request *req = cdev->req;
	int value = -EOPNOTSUPP;
	u16 w_index = le16_to_cpu(ctrl->wIndex);
	u16 w_value = le16_to_cpu(ctrl->wValue);
	u16 w_length = le16_to_cpu(ctrl->wLength);

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
	}
	/* respond with data transfer or status phase? */
	if (value >= 0) {
		pr_debug("audio req%02x.%02x v%04x i%04x l%d\n",
			ctrl->bRequestType, ctrl->bRequest,
			w_value, w_index, w_length);
		req->zero = 0;
		req->length = value;
		req->complete = audio_control_complete;
		value = usb_ep_queue(cdev->gadget->ep0, req, GFP_ATOMIC);
		if (value < 0)
			pr_err("audio response on err %d\n", value);
	}
```

```
static int audio_set_endpoint_req(struct usb_function *f,
		const struct usb_ctrlrequest *ctrl)
{
	int value = -EOPNOTSUPP;
	u16 ep = le16_to_cpu(ctrl->wIndex);
	u16 len = le16_to_cpu(ctrl->wLength);
	u16 w_value = le16_to_cpu(ctrl->wValue);
	pr_debug("bRequest 0x%x, w_value 0x%04x, len %d, endpoint %d\n",
			ctrl->bRequest, w_value, len, ep);
	switch (ctrl->bRequest) {
	case UAC_SET_CUR:
	case UAC_SET_MIN:
	case UAC_SET_MAX:
	case UAC_SET_RES:
		value = len;
		break;
	default:
		break;
	}
	return value;
}
```

c) f_gsi

- EP0 buffer allocated in composite.c is USB_COMP_EP0_BUFSIZ (4096) bytes large
- function's control transfer handler gsi_setup reads ctrl->wLength to w_length variable
- for bRequest set to USB_CDC_SEND_ENCAPSULATED_COMMAND value is set to w_length
- data transfer phase length is set to value; req->length = value;
- data transfer results in buffer overflow by wLength - 4096 bytes
- amount of data written to and past EP0 buffer is controller by attacker

```
static int
gsi_setup(struct usb_function *f, const struct usb_ctrlrequest *ctrl)
{
	struct f_gsi *gsi = func_to_gsi(f);
	struct usb_composite_dev *cdev = f->config->cdev;
	struct usb_request *req = cdev->req;
	int id, value = -EOPNOTSUPP;
	u16 w_index = le16_to_cpu(ctrl->wIndex);
	u16 w_value = le16_to_cpu(ctrl->wValue);
	u16 w_length = le16_to_cpu(ctrl->wLength);
	struct gsi_ctrl_pkt *cpkt;
	u8 *buf;
	u32 n;
	bool line_state;
    ...
    switch ((ctrl->bRequestType << 8) | ctrl->bRequest) {
    ...
	case ((USB_DIR_OUT | USB_TYPE_CLASS | USB_RECIP_INTERFACE) << 8)
			| USB_CDC_SEND_ENCAPSULATED_COMMAND:
		log_event_dbg("USB_CDC_SEND_ENCAPSULATED_COMMAND");
		if (w_value || w_index != id)
			goto invalid;
		/* read the request; process it later */
		value = w_length;
		req->context = gsi;
		if (gsi->prot_id == IPA_USB_RNDIS)
			req->complete = gsi_rndis_command_complete;
		else
			req->complete = gsi_ctrl_cmd_complete;
		/* later, rndis_response_available() sends a notification */
		break;
    ...
    ...
    /* respond with data transfer or status phase? */
	if (value >= 0) {
		log_event_dbg("req%02x.%02x v%04x i%04x l%d",
			ctrl->bRequestType, ctrl->bRequest,
			w_value, w_index, w_length);
		req->zero = (value < w_length);
		req->length = value;
		value = usb_ep_queue(cdev->gadget->ep0, req, GFP_ATOMIC);
		if (value < 0)
			log_event_err("response on err %d", value);
	}
```

d) f_mtp

- EP0 buffer allocated in composite.c is USB_COMP_EP0_BUFSIZ (4096) bytes large
- function's control transfer handler mtp_ctrlrequest reads ctrl->wLength to w_length
- for bRequest set to MTP_REQ_CANCEL value is set to w_length
- data transfer phase length is set to value; req->length = value;
- data transfer results in buffer overflow by wLength - 4096 bytes
- amount of data written to and past EP0 buffer is controller by attacker


```
static int mtp_ctrlrequest(struct usb_composite_dev *cdev,
				const struct usb_ctrlrequest *ctrl)
{
	struct mtp_dev *dev = _mtp_dev;
	int	value = -EOPNOTSUPP;
	u16	w_index = le16_to_cpu(ctrl->wIndex);
	u16	w_value = le16_to_cpu(ctrl->wValue);
	u16	w_length = le16_to_cpu(ctrl->wLength);
	unsigned long	flags;
    ...
    	} else if ((ctrl->bRequestType & USB_TYPE_MASK) == USB_TYPE_CLASS) {
		mtp_log("class request: %d index: %d value: %d length: %d\n",
			ctrl->bRequest, w_index, w_value, w_length);
		if (ctrl->bRequest == MTP_REQ_CANCEL && w_index == 0
				&& w_value == 0) {
			mtp_log("MTP_REQ_CANCEL\n");
			spin_lock_irqsave(&dev->lock, flags);
			if (dev->state == STATE_BUSY) {
				dev->state = STATE_CANCELED;
				wake_up(&dev->read_wq);
				wake_up(&dev->write_wq);
			}
			spin_unlock_irqrestore(&dev->lock, flags);
			/* We need to queue a request to read the remaining
			 *  bytes, but we don't actually need to look at
			 * the contents.
			 */
			value = w_length;
    ...
    /* respond with data transfer or status phase? */
	if (value >= 0) {
		int rc;
		cdev->req->zero = value < w_length;
		cdev->req->length = value;
		rc = usb_ep_queue(cdev->gadget->ep0, cdev->req, GFP_ATOMIC);
		if (rc < 0)
			pr_err("%s: response queue error\n", __func__);
	}
```

e) f_qc_rndis

- EP0 buffer allocated in composite.c is USB_COMP_EP0_BUFSIZ (4096) bytes large
- function's control transfer handler rndis_qc_setup reads ctrl->wLength to w_length
- for bRequest set to USB_CDC_SEND_ENCAPSULATED_COMMAND value is set to w_length
- data transfer phase length is set to value; req->length = value;
- data transfer results in buffer overflow by wLength - 4096 bytes
- amount of data written to and past EP0 buffer is controller by attacker

```
static int
rndis_qc_setup(struct usb_function *f, const struct usb_ctrlrequest *ctrl)
{
	struct f_rndis_qc		*rndis = func_to_rndis_qc(f);
	struct usb_composite_dev *cdev = f->config->cdev;
	struct usb_request	*req = cdev->req;
	int			value = -EOPNOTSUPP;
	u16			w_index = le16_to_cpu(ctrl->wIndex);
	u16			w_value = le16_to_cpu(ctrl->wValue);
	u16			w_length = le16_to_cpu(ctrl->wLength);
    ...
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
		req->complete = rndis_qc_command_complete;
		/* later, rndis_response_available() sends a notification */
		break;
    ...
	/* respond with data transfer or status phase? */
	if (value >= 0) {
		DBG(cdev, "rndis req%02x.%02x v%04x i%04x l%d\n",
			ctrl->bRequestType, ctrl->bRequest,
			w_value, w_index, w_length);
		req->context = rndis;
		req->zero = (value < w_length);
		req->length = value;
		value = usb_ep_queue(cdev->gadget->ep0, req, GFP_ATOMIC);
		if (value < 0)
			pr_err("rndis response on err %d\n", value);
	}
```

f) f_rmnet

- EP0 buffer allocated in composite.c is USB_COMP_EP0_BUFSIZ (4096) bytes large
- function's control transfer handler frmnet_setup reads ctrl->wLength to w_length
- for bRequest set to USB_CDC_SEND_ENCAPSULATED_COMMAND ret is set to w_length
- data transfer phase length is set to ret; req->length = ret;
- data transfer results in buffer overflow by wLength - 4096 bytes
- amount of data written to and past EP0 buffer is controller by attacker

```
static int
frmnet_setup(struct usb_function *f, const struct usb_ctrlrequest *ctrl)
{
	struct f_rmnet			*dev = func_to_rmnet(f);
	struct usb_composite_dev	*cdev = dev->cdev;
	struct usb_request		*req = cdev->req;
	u16				w_index = le16_to_cpu(ctrl->wIndex);
	u16				w_value = le16_to_cpu(ctrl->wValue);
	u16				w_length = le16_to_cpu(ctrl->wLength);
	int				ret = -EOPNOTSUPP;
    ...

	switch ((ctrl->bRequestType << 8) | ctrl->bRequest) {
	case ((USB_DIR_OUT | USB_TYPE_CLASS | USB_RECIP_INTERFACE) << 8)
			| USB_CDC_SEND_ENCAPSULATED_COMMAND:
		pr_debug("%s: USB_CDC_SEND_ENCAPSULATED_COMMAND\n"
				 , __func__);
		ret = w_length;
		req->complete = frmnet_cmd_complete;
		req->context = dev;
		break;
    ...
    /* respond with data transfer or status phase? */
	if (ret >= 0) {
		VDBG(cdev, "rmnet req%02x.%02x v%04x i%04x l%d\n",
			ctrl->bRequestType, ctrl->bRequest,
			w_value, w_index, w_length);
		req->zero = (ret < w_length);
		req->length = ret;
		ret = usb_ep_queue(cdev->gadget->ep0, req, GFP_ATOMIC);
		if (ret < 0)
			ERROR(cdev, "rmnet ep0 enqueue err %d\n", ret);
	}
```

## Impact

Devices implementing affected usb device gadget classes (f_accessory, f_audio_source, f_gsi, f_mtp, f_qc_rndis, f_rmnet) may be affected by buffer overflow vulnerabilities resulting in information disclosure, denial of service or execution of arbitrary code in kernel context.

## CVE

[CVE-2022-20009](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-20009)


## Exploit

Issuing control transfer requests with wLength greater than the standard 4096 bytes requires the host to use a custom build of libusb with MAX_CTRL_BUFFER_LENGTH increased to 0xffff. This value can be altered in libusb/os/linux_usbfs.h prior to build.

The gadget.py script requires pyusb. You can install this package via pip as below.

> python3 -m pip install pyusb

Help can be accessed with -h or --help parameters.

```
usage: gadget.py [-h] -v VID -p PID [-l LENGTH] [-d {read,write}] [-f {accessory,audio_source,gsi,qc_rndis,rmnet,mtp}]

Sample exploit for CVE-2022-20009

optional arguments:
  -h, --help            show this help message and exit
  -v VID, --vid VID     vendor id
  -p PID, --pid PID     product id
  -l LENGTH, --length LENGTH
                        lenght of data to write
  -d {read,write}, --direction {read,write}
                        direction of operation from host perspective
  -f {accessory,audio_source,gsi,qc_rndis,rmnet,mtp}, --function {accessory,audio_source,gsi,qc_rndis,rmnet,mtp}
```

Example invocations:
```
./gadget.py -v 0x1b67 -p 0x400c -f audio_source
./gadget.py -v 0x18d1 -p 0x4e23 -f mtp
```

## Final notes

Please update your Android to the latest stable version.

