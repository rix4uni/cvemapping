#!/bin/bash
#
# Author : Dr. Abhishek Ghosh
# GNU GPL 3.0
# https://thecustomizewindows.com
clear
if ! [ -x "$(type -P openssl)" ]; then
  echo "ERROR: script requires openssl"
  echo "For Debian and friends, get it with 'apt-get install openssl'"
  echo "For OS X with Homebrew, get it with 'brew install openssl'"
  exit 1
fi
echo "-------------------------------------------------------------------------------"
echo " "
echo "You Are Going To Run Basic Test For FREAK Attack (CVE-2015-0204)"
echo "\x1B[36mTHIS SCRIPT ONLY AUTOMATES, IT IS NOT A GOLD STANDARD TEST FOR MiTM"
echo "or CVE-2015-0204.\x1B[0m"
echo " "
echo "THIS SCRIPT DOES NOT SEND DATA TO NSA, FBI OR THEIR AGENTS."
echo "\x1B[36mIf Password is Asked, that is your username's password.\x1B[0m"
echo "This Script is Based on Akamai's Method as of 2nd March 2015, by Rich Salz"
echo "and Bill Brenner."
echo "Getting error means the server may be SAFE from FREAK Attack (CVE-2015-0204)"
echo "We suggest you to use nmap Tool, this is a basic openssl based script."
echo " "
echo "It is better to use any Free Software Like this one than testing on someone's Server"
echo "TO RAISE QUESTION ABOUT THIS SCRIPT'S POSSIBILITY OF BEING A SPYWARE"
echo "YOU MUST TAKE OPINION FROM RICHARD M. STALLMAN via email : \x1B[36mrms@gnu.org\x1B[0m"
echo "If you get better and simple way to test/script/method which is released as Free Software,"
echo "then contact via \x1B[36madmin@thecustomizewindows.com\x1B[0m"
echo ""
echo "-------------------------------------------------------------------------------"
echo " LEGAL "
echo " By Running This Script, You Are Agreeing That : "
echo " 1. You will test others' server ONLY once for personal usage."
echo " 2. You should not run this script to attack others' servers including"
echo " the example domains given below."
echo " 3. You are agreeing that, you'll not disturb the script"
echo " writer by raising any issue rather re-write a new script yourself."
echo "\x1B[36mIf you can not agree with these hit [N] key to disagree with us.\x1B[0m"
echo "Getting no error means the server may not be SAFE from FREAK Attack."
echo "Test these servers behind to get the idea of Right type of error:"
echo "\x1B[36mthecustomizewindows.com\x1B[0m"
echo "\x1B[36mblogs.akamai.com\x1B[0m"
echo "Regardless of the result, you should test on SSL Labs too."
read -p " Read the stuffs above first. To Run This Script hit [Y] or [N] Key " -n 1 -r
if [[ $REPLY =~ ^[Nn]$ ]]
then
echo " \x1B[36mYou typed N to quit.\x1B[0m Script Exited."
exit
fi
if [[ $REPLY =~ ^[Yy]$ ]]
then
echo "We are running this script with sudo privilege."
echo " "
echo "Type the domain name: (do not add http or https, you can paste the copied domain name)"
read domain
echo "Type the port: (normally 443 for HTTPS websites, you can paste the copied port)"
read port
echo " "
echo "-----------START OF TEST------------"
MOREF=`sudo openssl s_client -connect $domain:$port -cipher EXPORT | grep error`
finish=`date "+%Y-%m-%d-%H-%M-%S"`
echo "Test of $domain completed at ${finish} $MOREF"
echo "-----------END OF RESULT--------------"
echo ""
fi
