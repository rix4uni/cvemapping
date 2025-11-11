#!/bin/bash

# pve-script-wrapper.sh - Universal wrapper for Proxmox community scripts
# Automatically applies AppArmor workaround for CVE-2025-52881
#
# Usage: pve-script-wrapper.sh <script-url>
# Example: pve-script-wrapper.sh https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/komodo.sh

set -e

SCRIPT_URL="$1"

if [[ -z "$SCRIPT_URL" ]]; then
    cat <<EOF
Usage: $(basename "$0") <script-url>

Runs Proxmox community scripts with automatic AppArmor fix for Docker/containers.

Examples:
  $(basename "$0") https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/komodo.sh
  $(basename "$0") https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/docker.sh
  $(basename "$0") https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/dockge.sh

This wrapper addresses CVE-2025-52881 which breaks Docker in LXC containers.
See: https://github.com/opencontainers/runc/issues/4968
EOF
    exit 1
fi

# Verify we're running on Proxmox
if [[ ! -f "/usr/sbin/pct" ]]; then
    echo "Error: This script must be run on a Proxmox VE host"
    exit 1
fi

# Verify pct-patched exists
if [[ ! -f "/usr/local/bin/pct-patched" ]]; then
    echo "Error: /usr/local/bin/pct-patched not found"
    echo "Please ensure all wrapper components are installed"
    exit 1
fi

# Make pct-patched executable if it isn't already
chmod +x /usr/local/bin/pct-patched 2>/dev/null || true

echo "=========================================="
echo "Proxmox Script Wrapper with AppArmor Fix"
echo "=========================================="
echo "Script URL: $SCRIPT_URL"
echo "CVE-2025-52881 workaround: ENABLED"
echo ""

# Create temporary directory for our patched PATH
TEMP_BIN=$(mktemp -d)
trap "rm -rf '$TEMP_BIN'" EXIT

# Create symlink to our patched pct in temp directory
ln -s /usr/local/bin/pct-patched "$TEMP_BIN/pct"

# Download and execute the script with our patched PATH
echo "Downloading script..."
SCRIPT_CONTENT=$(curl -fsSL "$SCRIPT_URL")

echo "Executing script with AppArmor workaround..."
echo ""

# Export PATH with our wrapper first
export PATH="$TEMP_BIN:$PATH"

# Execute the downloaded script
bash -c "$SCRIPT_CONTENT"

EXIT_CODE=$?

echo ""
echo "=========================================="
if [[ $EXIT_CODE -eq 0 ]]; then
    echo "Script completed successfully!"
    echo "AppArmor fix has been applied to any containers created."
else
    echo "Script exited with code: $EXIT_CODE"
fi
echo "=========================================="

exit $EXIT_CODE
