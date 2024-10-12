#!/bin/sh

if [[ -f "$1/Contents/Info.plist" ]]; then
    CLIENT="$( /usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" "$1/Contents/Info.plist" )"
    CLIENT_TYPE=0
else
    CLIENT="$1"
    CLIENT_TYPE=1
fi

CAM_ACCESS="('kTCCServiceCamera', '${CLIENT}', ${CLIENT_TYPE}, 2, 2, 1, 0)"
MIC_ACCESS="('kTCCServiceMicrophone', '${CLIENT}', ${CLIENT_TYPE}, 2, 2, 1, 0)"
SQL_CMD="INSERT INTO access (service, client, client_type, auth_value, auth_reason, auth_version, flags) VALUES "
TCC_DB="${HOME}/Library/Application Support/com.apple.TCC/TCC.db"
TMPDIR="$(mktemp -d)"

cp "${TCC_DB}" "${TMPDIR}/TCC.db"
sqlite3 "${TMPDIR}/TCC.db" "DELETE FROM access WHERE service='kTCCServiceCamera' AND client='${CLIENT}'"
sqlite3 "${TMPDIR}/TCC.db" "DELETE FROM access WHERE service='kTCCServiceMicrophone' AND client='${CLIENT}'"
sqlite3 "${TMPDIR}/TCC.db" "${SQL_CMD}${CAM_ACCESS}"
sqlite3 "${TMPDIR}/TCC.db" "${SQL_CMD}${MIC_ACCESS}"
mv "${TMPDIR}/TCC.db" "${TCC_DB}"

echo "Granted camera and microphone access to $1"
