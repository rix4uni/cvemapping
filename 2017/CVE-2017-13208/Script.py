#!/usr/bin/python3.8
import sys
import r2pipe
from os import path


def print_error(error):
    #  warps print() in order to make errors unrepeatable and easier to maintain.
    print("[Error] " + error)
    exit()


def print_line(disassembly, index):
    # prints the given index's line from disassembly.
    while disassembly[index] != "\n":  # get to the beginning of the line.
        index -= 1

    index += 1  # skip "\n"
    line_begin = disassembly[index:] 
    print(line_begin.splitlines()[0])


def check_for_vulnerability(disassembly):
    # looks for dhcp_size validity checks in the given disassembly.
    vulnerable = True
    hex_values = ["0x4ec", "0x4f4"]  # first part of the validity check may have two forms.

    for hex_value in hex_values:
        index = disassembly.find(hex_value)
        if index != -1:
            print("[v] File not vulnerable, dhcp_size validity checks were found:")
            print_line(disassembly, index)

            index = disassembly.find("0x1c")  # second part of the validity check.
            print_line(disassembly, index)
            vulnerable = False
            break

    if vulnerable:  # if both forms of the validity check weren't found, declare the file as vulnerable.
        print("[x] File is vulnerable, dhcp_size validity checks were not found.:")
        index = disassembly.find("memcpy")  # locate the location of memcpy() in the disassembly.
        print_line(disassembly, index)
        exit()


def main():
    if len(sys.argv) != 2:  # check for correct usage.
        print_error(f"Usage: {sys.argv[0]} <file_path>")

    file_path = sys.argv[1]
    if not path.exists(file_path):  # validate input path.
        print_error(f"{file_path} doesn't exist.")

    if not file_path.endswith(".so"):  # validate input format.
        print_error("Wrong format.")

    command = 'sym.receive_packet'

    binary = r2pipe.open(file_path)
    binary.cmd('aa')  # analyze all.

    disassembly = binary.cmd('pdf @ ' + command)
    check_for_vulnerability(disassembly)


if __name__ == "__main__":  # entry point.
    main()
