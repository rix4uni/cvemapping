#!/bin/bash

TARGET_APP_CMDLINE="/System/Applications/Music.app/Contents/MacOS/Music -quitAfterLaunch"
#TARGET_APP_CMDLINE="/System/Applications/Music.app/Contents/MacOS/Music"

# NOTE: Since we only target Cache.db for now, leave the rest of them alone!
killall Music
rm -f "/Users/$(whoami)/Library/Caches/com.apple.Music/Cache.db"
#rm -f "/Users/$(whoami)/Library/HTTPStorages/com.apple.Music/httpstorages.sqlite"
#rm -f "/Users/$(whoami)/Music/Music/Music Library.musiclibrary/Extras.itdb"
#rm -f "/Users/$(whoami)/Music/Music/Music Library.musiclibrary/Genius.itdb"
#rm -f "/Users/$(whoami)/Library/Application Support/com.apple.MediaPlayer/ServerObjectDatabases/com.apple.Music-ServerObjectDatabase.sqlpkg/Database"
#rm -f "/Users/$(whoami)/Library/Caches/com.apple.Music/MusicUIArtworkCache/Cache.db"
#rm -f "/Users/$(whoami)/Library/Caches/com.apple.AppleMediaServices/Metrics/Music/metrics.sqlitedb"

$TARGET_APP_CMDLINE 1>/dev/null 2>/dev/null &
CHILDPID=$!
echo "[?] Child pid: $CHILDPID"
echo "[+] Waiting for max 3s"
timeout=1
for i in $(seq 3)
do
	running=$(ps | grep $CHILDPID | grep -v grep | wc -l)
	if [[ running -eq 0 ]]
	then
		echo "[+] Music stopped"
		timeout=0
		break
	fi
	echo "Sleeping... $i"
	sleep 1
done

if [[ timeout -eq 1 ]]
then
	echo "[+] Timeout reached, killing Music"
	kill $CHILDPID
	sleep 1
fi

