# BadBlue (Windows)


CVE-2024-21306 BadBlue implementation (Using DuckyScript)

Unauthenticated Peering Leading to Code Execution (Using HID Keyboard)

[This is an implementation of the CVE discovered by marcnewlin](https://github.com/marcnewlin/hi_my_name_is_keyboard)

[And some code from BlueDucky](https://github.com/pentestfunctions/BlueDucky)

## Introduction
BadBlue is a powerful tool for exploiting a vulnerability in Bluetooth devices. By running this script, you can:

1. Load saved Bluetooth devices that are no longer visible but have Bluetooth still enabled.
2. Automatically save any devices you scan.
3. Send payload via ducky script format to interact with devices.

I've successfully run this on any Raspberry Pi 4 and VirtualBox using the CSR 4.0, ORICO 4.0,.. Bluetooth module. It works against various Windows with version lower .3007 .
The Windows computer must be paired with a Bluetooth keyboard, and the keyboard must be switched off (or out of range).

An attacker, using an Ubuntu (Kali can run but not recommend) computer and Broadcom-based Bluetooth adapter (CSR 4.0 maybe can run), spoofs the address of the target keyboard and connects to L2CAP 17 on the Windows computer, while specifying the `NoInputNoOutput` SSP pairing-capability.

The victim will see a notification reading `Add a device` `Tap to set up your <Keyboard Name>`.

If they ignore the notification, nothing will happen.

If they click on the notification, they will be presented with a Bluetooth pairing-request dialog.

If the victim has the `Add a Bluetooth device` UI open, they will not see a notification, and will instead be immediately presented with the pairing-request as a modal dialog.

The attacker can complete pairing once the pairing-request dialog closes, even if the user clicks `Cancel` or `X`. Once pairing completes, the attacker connects to L2CAP 17 (HID Control).

The attacker then can connect to L2CAP 19 (HID Interrupt), and is able to inject arbitrary keystrokes.

## Installation and Usage

### Setup Instructions

```bash
# update apt
sudo apt-get update && sudo apt-get -y upgrade

# install dependencies from apt
sudo apt install -y bluez-tools bluez-hcidump git \
                    python3-pip python3-setuptools \
                    libbluetooth-dev dbus-x11

# configure bluetoothd to run in compatibility mode to support sdptool
sudo sed -i "s|ExecStart=/usr/lib/bluetooth/bluetoothd|ExecStart=/usr/lib/bluetooth/bluetoothd --compat|g" /lib/systemd/system/bluetooth.service
sudo systemctl daemon-reload
sudo systemctl restart bluetooth

# install pybluez
git clone https://github.com/pybluez/pybluez.git
cd pybluez
sudo python3 setup.py install
python3 -m pip install pydbus

# build bdaddr from bluez
cd ~
git clone https://github.com/bluez/bluez.git
cd bluez
gcc -o bdaddr tools/bdaddr.c src/oui.c -lbluetooth -I.
sudo cp bdaddr /usr/local/bin/
```

## Running BadBlue
```bash
# clone this repository
git clone https://github.com/PhucHauDeveloper/BadBlue.git
cd BadBlue
python3 BadBlue.py
```

1. Pair a Bluetooth keyboard to the target Windows-computer, and turn off the keyboard
2. On the Ubuntu computer, run the PoC: `./BadBlue.py -i <Interface> -k <Keyboard-Address> -c <Windows-Address>`
3. Click on the notification when it appears on the Windows computer
4. Close the pairing-request dialog (or click `Cancel` or `Approve`)
5. If successful, the Ubuntu machine will connect to the Windows machine and inject a nondestructive your payload
   
`-k` is keyboard (default my keyboard `F4:73:35:7A:4B:BB`, you need change it)

`-i` is interface (default hci0)

`-c` is target windows devices (type blank tool auto scan for you)


## Duckyscript
Work in Progress:
- Suggest me ideas

## Know Bug
Maybe your first time using and readchar is missing, use the following command:
```
pip install readchar
```
This tool should run in a GUI environment, CLI can cause dbus-launch error, if you know how to fix it contact me.

#### Example payload.txt:
```bash
REM Title of the payload
STRING ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_-=+\|[{]};:'",<.>/?
GUI D
```

```bash
REM Opens RickRoll
DELAY 200
GUI r
DELAY 200
STRING https://www.youtube.com/watch?v=dQw4w9WgXcQ
DELAY 300
ENTER
DELAY 300
```

## Enjoy experimenting with BadBlue!


