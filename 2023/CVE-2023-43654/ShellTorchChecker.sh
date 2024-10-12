#!/bin/bash

TORCHSERVE_PORT=8081
TORCHSERVE_IP=""
RUNNING_RESPONSE='{"code":400,"type":"BadRequestException","message":"Parameterurlisrequired."}'
PROCESS_IS_RUNNING=false
PROCESS_NAME="torchserve"
LOCALHOST_IPV4="127.0.0.1"
LOCALHOST_STR="localhost"

# RESULT ARGS
IS_ACCESIBLE=false
HAS_SSRF=false


if [[ "$TERM_PROGRAM" == "iTerm.app" ]]; then
  # iTerm2 escape codes for colors
  COLOR_RED="\033[38;5;196m"
  COLOR_GREEN="\033[38;5;40m"
  COLOR_YELLOW="\033[38;5;226m"
  COLOR_WHITE="\033[38;5;15m"
  TEXT_BOLD="\033[1m"
  NORMAL_TEXT="\033[0m"
  TEXT_UNDERLINE="\033[4m"
else
  # ANSI escape codes for colors
  COLOR_RED="\e[31m"
  COLOR_GREEN="\e[32m"
  COLOR_YELLOW="\e[93m"
  COLOR_WHITE="\e[0m"
  TEXT_BOLD="\e[1m"
  NORMAL_TEXT="\e[0m"
  TEXT_UNDERLINE="\e[4m"
fi



COLOR_RED_FORMAT="    $COLOR_RED[X] "
COLOR_GREEN_FORMAT="    $COLOR_GREEN[V] "
COLOR_YELLOW_FORMAT="    $COLOR_YELLOW[] "
COLOR_WHITE_FORMAT="  $COLOR_WHITE[-] "


####################### SSRF PARAMETERS ################################################
SSRF_DOWNLOAD_FILE_NAME="OligoTest.tar.gz"
REMOTE_SERVER="https://raw.githubusercontent.com/OligoCyberSecurity/ShellTorchChecker/main"
# We don't really want to download any valid workflow to the server. If we get this error TorchServe tries to download the file 
SSRF_RESPONSE='{"code":500,"type":"IOException","message":"Inputisnotinthe.gzformat"}'
# This response is returned if this script ran twice
SSRF_RESPONSE_EXISTS="{\"code\":500,\"type\":\"FileAlreadyExistsException\",\"message\":\"$SSRF_DOWNLOAD_FILE_NAME\"}"
SSRF_NOT_VULNERABLE_RESPONSE="{\"code\":404,\"type\":\"WorkflowNotFoundException\",\"message\":\"GivenURL${REMOTE_SERVER}/${SSRF_DOWNLOAD_FILE_NAME}doesnotmatchanyallowedURL(s)\"}"
########################################################################################
echo "
 _____  _    _ ______ _      _   _______ ____  _____   _____ _    _ 
/ ____ | |  | |  ____| |    | | |__   __/ __ \|  __ \ / ____| |  | |
| (___ | |__| | |__  | |    | |    | | | |  | | |__) | |    | |__| |
\___  \|  __  |  __| | |    | |    | | | |  | |  _  /| |    |  __  |
____)  | |  | | |____| |____| |____| | | |__| | | \ \| |____| |  | |
|_____/|_|  |_|______|______|______|_|  \____/|_|  \_\\______|_|  |_|
                                                                     
                                                                     "

if [ $# -lt 1 ]; then
  echo "Usage: ShellTorchChecker.sh <IP_ADDRESS>"
  exit 1
fi

TORCHSERVE_IP="$1"

echo "This script checks for TorchServe CVE-2023-43654"
echo "The vulnerability was found by the Oligo research team and allows for No-Auth RCE"
echo "For more details please see our full report at https://www.oligo.security/blog/shelltorch-torchserve-ssrf-vulnerability-cve-2023-43654"
echo ""
echo "Disclaimer:"
echo "By using this tool, you acknowledge and agree that it is provided \"as is\" without"
echo "warranty of any kind, either express or implied. Oligo and any contributors shall not be held"
echo "liable for any direct, indirect, incidental, or consequential damages or false results arising"
echo "out of the use, misuse, or reliance on this tool."
echo "You are solely responsible for understanding the output and implications of using this tool"
echo "and for any actions taken based on its findings."
echo "Use at your own risk."
echo "..........................................."
echo "By continuing running this script I agree that I have read the disclaimer and have agreed to it."
echo "Press any key to start scanning, Press Ctrl+C to exit."
read -n 1 -s
echo ""

####################### Pre-checks #####################################################
# If TorchServe ip is 127.0.0.1
if [ "$TORCHSERVE_IP" = "$LOCALHOST_IPV4" ] || [ "$TORCHSERVE_IP" = "$LOCALHOST_STR" ]; then
  # Check if TorchServe is running on this machine
  if ps aux | grep -v grep | grep "$PROCESS_NAME" > /dev/null; then
    echo "$PROCESS_NAME is running locally."
    PROCESS_IS_RUNNING=true
  else
    echo "$PROCESS_NAME is not running locally."
    PROCESS_IS_RUNNING=false
  fi
fi
########################################################################################
echo -e "${TEXT_BOLD}Scan Results:${NORMAL_TEXT}"
####################### Test port listen configuration #################################
echo -e "${COLOR_WHITE_FORMAT}Checking Management Interface API Misconfiguration (port $TORCHSERVE_PORT)"

# IF running locally
if [ "$PROCESS_IS_RUNNING" = true ]; then
  # Check if the port is open on all interfaces
  ss -tuln | grep -q "0.0.0.0:$TORCHSERVE_PORT"
  # Check the exit status of the previous command
  if [ $? -eq 0 ]; then
    IS_ACCESIBLE=true
  else
    IS_ACCESIBLE=false
  fi


# IF running remote
else
  test_response=$(curl -s -X POST http://$TORCHSERVE_IP:$TORCHSERVE_PORT/workflows)
  test_response=$(echo "$test_response" | tr -d '[:space:]')
  if [[ "$test_response" == "$RUNNING_RESPONSE" ]]; then
    IS_ACCESIBLE=true
  else
    IS_ACCESIBLE=false
  fi
fi

# Print result
if  [ "$IS_ACCESIBLE" = true ]; then
  echo -e "${COLOR_RED_FORMAT}${TORCHSERVE_IP}:${TORCHSERVE_PORT} is open to remote connections"
else
  echo -e "${COLOR_GREEN_FORMAT}${TORCHSERVE_IP}:${TORCHSERVE_PORT} is not open to remote connections"
fi
########################################################################################


####################### Test for SSRF CVE-2023-43654 ###################################
response=$(curl --max-time 10 -s -X POST http://$TORCHSERVE_IP:$TORCHSERVE_PORT/workflows\?url\=$REMOTE_SERVER/$SSRF_DOWNLOAD_FILE_NAME)
response=$(echo "$response" | tr -d '[:space:]')
echo -e "${COLOR_WHITE_FORMAT}Checking CVE-2023-43654 Remote Server-Side Request Forgery (SSRF)"

# If no response at all
if [ -z "$response" ]; then
  echo -e "${COLOR_YELLOW_FORMAT}Cannot check CVE-2023-43654 Failed to send request to http://$TORCHSERVE_IP:$TORCHSERVE_PORT"

# Check response
else
  if [[ "$response" == "$SSRF_RESPONSE_EXISTS" ]]; then
    echo -e "${COLOR_YELLOW_FORMAT}The test file already exists in the server.To test again remove the file <torchserve_path>model-server/model-store/$SSRF_DOWNLOAD_FILE_NAME and run the script."
    HAS_SSRF=true
  elif [[ "$response" == "$SSRF_RESPONSE" ]]; then
    HAS_SSRF=true
    echo -e "${COLOR_RED_FORMAT}Vulnerable to CVE-2023-43654 SSRF file download"
  elif [[ "$response" == "$SSRF_NOT_VULNERABLE_RESPONSE" ]]; then
    HAS_SSRF=false
    echo -e "${COLOR_GREEN_FORMAT}Not Vulnerable to CVE-2023-43654 SSRF file download"
  else
    HAS_SSRF=true
    echo -e "${COLOR_YELLOW_FORMAT}Could not determine if TorchServe is vulnerable to CVE-2023-43654"
  fi
fi
########################################################################################
if [ "$IS_ACCESIBLE" = true ] || [ "$HAS_SSRF" = true ]; then
  echo ""
  echo -e "${COLOR_WHITE}${TEXT_BOLD}Recommendations:${NORMAL_TEXT}"
  if [ "$IS_ACCESIBLE" = true ]; then
    echo -e "${COLOR_WHITE_FORMAT}To resolve Management Interface API Misconfiguration:
      Change \"management_address\" in config.properties from 0.0.0.0 to 127.0.0.1"
    echo -e "      ${TEXT_UNDERLINE}example:${COLOR_WHITE}${NORMAL_TEXT}"
    echo -e "        management_address: http://127.0.0.1:8081"
  fi
  if [ "$HAS_SSRF" = true ]; then
    echo -e "${COLOR_WHITE_FORMAT}To resolve CVE-2023-43654 SSRF file download:
      Configure specific urls in the \"allowed_urls\" field of config.properties."
    echo -e "      ${TEXT_UNDERLINE}example:${COLOR_WHITE}${NORMAL_TEXT}"
    echo -e "        allowed_urls=https://s3.amazonaws.com/.*,https://torchserve.pytorch.org/.*"
  fi
fi
