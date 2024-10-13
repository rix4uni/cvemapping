import re
import os
import subprocess


def check_for_write(file_path):
    """
    check if we have write access to the file
    """
    if os.access(file_path, os.R_OK):
        return True
    return False


def check_versions():
    """
    check the systemctl version and the polykit version
    """
    # these are the versions that where firstly reported
    # so we'll go with these and below
    max_version_ctl = "239"
    max_version_poly = "115"
    data_ctl = subprocess.check_output(["systemctl", "--version"])
    data_poly = subprocess.check_output(["pkttyagent", "--version"])
    results_ctl = data_ctl.split(" ")
    results_poly = data_poly.split(" ")
    vnum_ctl = results_ctl[1].split("\n")[0]
    vnum_poly = results_poly[-1].split(".")[-1]
    if vnum_ctl <= max_version_ctl:
        if vnum_poly <= max_version_poly:
            return True
        else:
            return False
    return False


def check_for_uid(file_path):
    """
    check to see if there are any users that are already compromised
    """
    retval = []
    # trial and error is a pain in the ass
    max_int = 2999999999
    searcher = re.compile(r"\b(\d+)\b")
    with open(file_path) as data:
        for line in data.readlines():
            if searcher.search(line) is not None:
                splitter = line.split(":")
                uid = splitter[2]
                try:
                    if int(uid) > int(max_int):
                        retval.append(line.strip())
                except:
                    pass
    if len(retval) != 0:
        return retval
    return None


def main():
    """
    main function
    """
    file_path = "/etc/passwd"

    version_in_target_scope = check_versions()
    write_access_to_file = check_for_write(file_path)
    possible_compromises = check_for_uid(file_path)

    if write_access_to_file:
        print("[+] you have write access to {}".format(file_path))
    else:
        print("[x] you do not have write access to {}".format(file_path))
    if version_in_target_scope:
        print("[+] versions appear to be within the vulnerable version scope")
    else:
        print("[x] versions are not in the vulnerable version scope")
    if possible_compromises is not None and version_in_target_scope:
        print("[+] total of {} possibly compromised user account(s)".format(len(possible_compromises)))
        for user in possible_compromises:
            print(user)
    else:
        print("[x] no compromised accounts created")


if __name__ == "__main__":
    main()