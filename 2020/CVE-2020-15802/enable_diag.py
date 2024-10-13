import socket

hci0 = 0
hci1 = 1
hci2 = 2

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)

# NOTE: usually devboard is assigned to HCI1
s.bind((hci1, ))

# NOTE: enable LMP and LE LL log
s.send(b"\x07\xf0\x01")

s.close()
