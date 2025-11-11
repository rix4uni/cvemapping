#!/bin/bash

# Quick installer for Proxmox LXC AppArmor Fix
# Usage: curl -fsSL https://raw.githubusercontent.com/jq6l43d1/proxmox-lxc-docker-fix/main/install.sh | bash

set -e

REPO_URL="https://raw.githubusercontent.com/jq6l43d1/proxmox-lxc-docker-fix/main"
INSTALL_DIR="/usr/local/bin"

echo "=========================================="
echo "Proxmox LXC AppArmor Fix Installer"
echo "=========================================="
echo ""

# Check if running on Proxmox
if [[ ! -f "/usr/sbin/pct" ]]; then
    echo "Error: This must be run on a Proxmox VE host"
    exit 1
fi

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root"
   exit 1
fi

echo "Installing to: $INSTALL_DIR"
echo ""

# Download scripts
echo "Downloading pve-script-wrapper.sh..."
curl -fsSL "$REPO_URL/pve-script-wrapper.sh" -o "$INSTALL_DIR/pve-script-wrapper.sh"

echo "Downloading pct-patched..."
curl -fsSL "$REPO_URL/pct-patched" -o "$INSTALL_DIR/pct-patched"

echo "Downloading pve-docker-fix..."
curl -fsSL "$REPO_URL/pve-docker-fix" -o "$INSTALL_DIR/pve-docker-fix"

# Make executable
echo "Setting permissions..."
chmod +x "$INSTALL_DIR/pve-script-wrapper.sh"
chmod +x "$INSTALL_DIR/pct-patched"
chmod +x "$INSTALL_DIR/pve-docker-fix"

echo ""
echo "=========================================="
echo "✓ Installation complete!"
echo "=========================================="
echo ""
echo "Usage:"
echo "  Run community scripts with fix:"
echo "    pve-script-wrapper.sh <script-url>"
echo ""
echo "  Fix existing containers:"
echo "    pve-docker-fix <container-id>"
echo ""
echo "Examples:"
echo "  pve-script-wrapper.sh https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/komodo.sh"
echo "  pve-docker-fix 105"
echo ""
echo "For more info: https://github.com/jq6l43d1/proxmox-lxc-docker-fix"
echo ""
