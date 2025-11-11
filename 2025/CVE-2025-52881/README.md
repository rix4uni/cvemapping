# Proxmox LXC AppArmor Fix for Docker/Containers

> **Workaround for CVE-2025-52881**: Fixes Docker, Podman, and container runtime breakage in Proxmox LXC containers caused by AppArmor incompatibility with runc 1.2.7+/1.3.2+

## 🚨 The Problem

Recent security updates to `runc` (versions 1.2.7+ and 1.3.2+) and `containerd` (1.7.28-2+) introduced a breaking incompatibility with AppArmor when running inside Proxmox LXC containers. This causes Docker and other container runtimes to fail with errors like:

```
OCI runtime create failed: unable to start container process:
error during container init: open sysctl net.ipv4.ip_unprivileged_port_start file:
reopen fd 8: permission denied
```

This affects:
- ✗ Proxmox community scripts (docker.sh, komodo.sh, dockge.sh, casaos.sh, etc.)
- ✗ Manual Docker/Podman installations in LXC
- ✗ Any container runtime using runc inside LXC containers

**Reference**: [opencontainers/runc#4968](https://github.com/opencontainers/runc/issues/4968)

## ⚠️ DO NOT Downgrade runc

While downgrading runc below 1.2.7/1.3.2 would "fix" the issue, it exposes your system to **actual privilege escalation vulnerabilities** that the security update patched. The workaround in this repository is the recommended approach.

## ✅ The Solution

This repository provides three tools that automatically apply the AppArmor workaround to Proxmox LXC containers:

1. **`pve-script-wrapper.sh`** - Universal wrapper for Proxmox community scripts
2. **`pve-docker-fix`** - Fix existing containers that are already broken
3. **`pct-patched`** - Internal wrapper (used automatically by pve-script-wrapper.sh)

### How It Works

The scripts automatically add these configuration lines to LXC containers:

```conf
lxc.apparmor.profile: unconfined
lxc.mount.entry: /dev/null sys/module/apparmor/parameters/enabled none bind 0 0
```

This disables AppArmor for the container and masks the AppArmor module, allowing runc to function correctly.

## 📦 Installation

On your Proxmox VE host, run:

```bash
# Download all scripts
curl -fsSL https://raw.githubusercontent.com/jq6l43d1/proxmox-lxc-docker-fix/main/pve-script-wrapper.sh -o /usr/local/bin/pve-script-wrapper.sh
curl -fsSL https://raw.githubusercontent.com/jq6l43d1/proxmox-lxc-docker-fix/main/pct-patched -o /usr/local/bin/pct-patched
curl -fsSL https://raw.githubusercontent.com/jq6l43d1/proxmox-lxc-docker-fix/main/pve-docker-fix -o /usr/local/bin/pve-docker-fix

# Make them executable
chmod +x /usr/local/bin/pve-script-wrapper.sh /usr/local/bin/pct-patched /usr/local/bin/pve-docker-fix
```

Or clone the repository:

```bash
git clone https://github.com/jq6l43d1/proxmox-lxc-docker-fix.git
cd proxmox-lxc-docker-fix
chmod +x *.sh pct-patched pve-docker-fix
cp pve-script-wrapper.sh pct-patched pve-docker-fix /usr/local/bin/
```

## 🚀 Usage

### Running Community Scripts with Automatic Fix

Instead of:
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/komodo.sh)"
```

Use:
```bash
pve-script-wrapper.sh https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/komodo.sh
```

This works with **any** Proxmox community script that creates LXC containers:

```bash
# Docker
pve-script-wrapper.sh https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/docker.sh

# Dockge
pve-script-wrapper.sh https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/dockge.sh

# CasaOS
pve-script-wrapper.sh https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/casaos.sh

# Podman
pve-script-wrapper.sh https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/podman.sh

# And any other script that installs container runtimes
```

### Fixing Existing Containers

If you already have a broken container:

```bash
# Fix container 105
pve-docker-fix 105

# Fix without automatic restart
pve-docker-fix 105 --no-restart
```

The tool will:
1. Check if the fix is already applied
2. Stop the container (with confirmation)
3. Apply the AppArmor workaround
4. Restart the container

### Manual Fix

If you prefer to apply the fix manually:

```bash
# Stop the container
pct stop 105

# Edit the config file
nano /etc/pve/lxc/105.conf

# Add these lines at the end:
lxc.apparmor.profile: unconfined
lxc.mount.entry: /dev/null sys/module/apparmor/parameters/enabled none bind 0 0

# Start the container
pct start 105
```

## 🔧 How It Works Technically

### pve-script-wrapper.sh
- Creates a temporary directory with a symlink to `pct-patched`
- Modifies `PATH` to prioritize the wrapper
- Downloads and executes the community script
- The script transparently uses the patched `pct` command

### pct-patched
- Intercepts `pct create` commands
- Calls the real `/usr/sbin/pct` to create the container
- Immediately after creation, injects AppArmor configuration into `/etc/pve/lxc/$CTID.conf`
- Passes through all other `pct` commands unchanged

### pve-docker-fix
- Standalone tool for fixing existing containers
- Checks if fix is already applied (idempotent)
- Handles container stop/start with user confirmation
- Safe to run multiple times

## 🛡️ Security Considerations

### What This Changes
- Disables AppArmor confinement for the LXC container
- Removes one layer of defense-in-depth

### What's Still Protected
- Container is still **unprivileged** (most important security boundary)
- Kernel namespaces still enforce isolation
- cgroups resource limits still apply
- Standard Linux permissions still active

### Risk Assessment
- **Risk**: Slightly reduced isolation if container is compromised
- **Mitigation**: Containers remain unprivileged, which is the primary security control
- **Comparison**: Much safer than downgrading runc and exposing actual CVEs

### When NOT to Use This
- Production environments requiring maximum isolation
- Multi-tenant systems with untrusted containers
- Containers running untrusted code

### Alternatives
- Wait for upstream fixes (Proxmox/LXC/AppArmor/kernel)
- Use privileged containers (NOT recommended - worse security)
- Use VMs instead of containers (more overhead)

## 📋 Affected Systems

### Confirmed Affected
- Proxmox VE 8.x with recent updates
- Debian 12 (Bookworm) LXC containers
- runc versions 1.2.7+ and 1.3.2+
- containerd version 1.7.28-2+

### Community Scripts Known to Be Affected
- docker.sh
- komodo.sh
- dockge.sh
- casaos.sh
- podman.sh
- runtipi.sh
- omv.sh (OpenMediaVault)
- alpine-docker.sh
- podman-homeassistant.sh
- And 390+ other container-based scripts

## 🔗 References

- **Primary Issue**: [opencontainers/runc#4968](https://github.com/opencontainers/runc/issues/4968)
- **CVE**: CVE-2025-52881
- **Related CVEs**: CVE-2025-31133, CVE-2025-52565
- **Proxmox Forum Discussion**: [Community Scripts Issue #8890](https://github.com/community-scripts/ProxmoxVE/issues/8890)
- **Incus Fix**: [PR #2624](https://github.com/lxc/incus/pull/2624)

## 🐛 Troubleshooting

### Script doesn't work
```bash
# Verify scripts are executable
ls -l /usr/local/bin/pve-script-wrapper.sh /usr/local/bin/pct-patched

# Make them executable if needed
chmod +x /usr/local/bin/pve-script-wrapper.sh /usr/local/bin/pct-patched
```

### Docker still fails after applying fix
```bash
# Verify the fix was applied
grep -i apparmor /etc/pve/lxc/105.conf

# If not present, apply manually
pve-docker-fix 105

# Check container is restarted
pct status 105
```

### Container won't start after fix
```bash
# Check for syntax errors in config
cat /etc/pve/lxc/105.conf

# View detailed error messages
journalctl -xe
```

## 🤝 Contributing

Contributions welcome! Please:
1. Test your changes on a Proxmox VE system
2. Update documentation if adding features
3. Follow existing code style
4. Submit a PR with clear description

## 📝 License

GNU GENERAL PUBLIC LICENSE - See LICENSE file for details

## 🙏 Acknowledgments

- [opencontainers/runc](https://github.com/opencontainers/runc) team for the security fixes
- [community-scripts/ProxmoxVE](https://github.com/community-scripts/ProxmoxVE) maintainers
- All contributors to the issue discussions

## ⚡ Quick Reference

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/jq6l43d1/proxmox-lxc-docker-fix/main/install.sh | bash

# Run community script with fix
pve-script-wrapper.sh <script-url>

# Fix existing container
pve-docker-fix <container-id>

# Get help
pve-script-wrapper.sh --help
pve-docker-fix --help
```

---

**Note**: This is a temporary workaround until upstream projects release permanent fixes. Monitor the referenced GitHub issues for updates.
