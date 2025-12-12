#!/bin/bash
#
# Next.js Security Update Script
# Addresses CVE-2025-55183, CVE-2025-55184, CVE-2025-67779
#
# Usage:
#   ./nextjs-security-update.sh              # Interactive account selection
#   ./nextjs-security-update.sh user1 org1   # Specify accounts directly
#
# Requirements: gh (GitHub CLI), jq, git
#
# Based on Next.js Security Advisory: December 11, 2025
# https://nextjs.org/blog/cve-2025-55183-and-cve-2025-55184

set -euo pipefail

WORK_DIR="${NEXTJS_UPDATE_DIR:-$HOME/nextjs-security-updates}"
LOG_FILE="$WORK_DIR/upgrade-log.txt"
DRY_RUN="${DRY_RUN:-false}"
AUTO_PUSH="${AUTO_PUSH:-false}"

# Colors (disabled if not a terminal)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    BOLD='\033[1m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' BLUE='' BOLD='' NC=''
fi

log()     { echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"; }
success() { echo -e "${GREEN}[OK]${NC} $1" | tee -a "$LOG_FILE"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$LOG_FILE"; }
error()   { echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"; }

usage() {
    cat << EOF
${BOLD}Next.js Security Update Script${NC}
Addresses CVE-2025-55183 (Source Code Exposure), CVE-2025-55184 (DoS), CVE-2025-67779 (Complete DoS Fix)

${BOLD}Usage:${NC}
  $0                           Interactive mode - select from your GitHub accounts
  $0 <user> [user2] [org1]     Process specified GitHub users/orgs

${BOLD}Environment Variables:${NC}
  NEXTJS_UPDATE_DIR    Work directory (default: ~/nextjs-security-updates)
  DRY_RUN=true         Show what would be done without making changes
  AUTO_PUSH=true       Automatically push changes after committing

${BOLD}Examples:${NC}
  $0 myusername myorg
  DRY_RUN=true $0 myusername
  AUTO_PUSH=true $0 myusername

${BOLD}Fixed Versions (per Next.js Advisory Dec 11, 2025):${NC}
  13.x, 14.0.x, 14.1.x  -> 14.2.35
  14.2.x                -> 14.2.35
  15.0.x                -> 15.0.7
  15.1.x                -> 15.1.11
  15.2.x                -> 15.2.8
  15.3.x                -> 15.3.8
  15.4.x                -> 15.4.10
  15.5.x                -> 15.5.9
  15.x canary           -> 15.6.0-canary.60
  16.0.x                -> 16.0.10
  16.x canary           -> 16.1.0-canary.19
EOF
    exit 0
}

check_dependencies() {
    local missing=()
    command -v gh &>/dev/null || missing+=("gh (GitHub CLI)")
    command -v jq &>/dev/null || missing+=("jq")
    command -v git &>/dev/null || missing+=("git")

    if [[ ${#missing[@]} -gt 0 ]]; then
        error "Missing dependencies: ${missing[*]}"
        echo "Install with:"
        echo "  brew install gh jq git     # macOS"
        echo "  sudo apt install gh jq git # Debian/Ubuntu"
        echo "  sudo pacman -S github-cli jq git # Arch"
        exit 1
    fi

    if ! gh auth status &>/dev/null; then
        error "GitHub CLI not authenticated. Run: gh auth login"
        exit 1
    fi
}

# Discover all available GitHub accounts (user + orgs)
discover_accounts() {
    local accounts=()

    # Get authenticated user
    local user
    user=$(gh api user --jq '.login' 2>/dev/null) || true
    [[ -n "$user" ]] && accounts+=("$user")

    # Get user's organizations
    while IFS= read -r org; do
        [[ -n "$org" ]] && accounts+=("$org")
    done < <(gh api user/orgs --jq '.[].login' 2>/dev/null || true)

    printf '%s\n' "${accounts[@]}"
}

# Interactive account selection
select_accounts() {
    local -a available=()
    local -a selected=()

    echo -e "${BOLD}Discovering GitHub accounts...${NC}" >&2

    while IFS= read -r account; do
        [[ -n "$account" ]] && available+=("$account")
    done < <(discover_accounts)

    if [[ ${#available[@]} -eq 0 ]]; then
        error "No GitHub accounts found. Check: gh auth status"
        exit 1
    fi

    {
        echo ""
        echo -e "${BOLD}Available GitHub accounts:${NC}"
        echo ""
        for i in "${!available[@]}"; do
            printf "  %d) %s\n" "$((i+1))" "${available[$i]}"
        done
        echo ""
        echo -e "${YELLOW}Enter numbers to scan (space-separated), 'a' for all, or 'q' to quit:${NC}"
        echo "Example: 1 3 4"
        echo ""
    } >&2

    read -r -p "> " selection </dev/tty

    if [[ "$selection" == "q" ]]; then
        echo "Cancelled."
        exit 0
    fi

    if [[ "$selection" == "a" || "$selection" == "all" ]]; then
        selected=("${available[@]}")
    else
        for num in $selection; do
            if [[ "$num" =~ ^[0-9]+$ ]] && [[ "$num" -ge 1 ]] && [[ "$num" -le "${#available[@]}" ]]; then
                selected+=("${available[$((num-1))]}")
            fi
        done
    fi

    if [[ ${#selected[@]} -eq 0 ]]; then
        error "No valid accounts selected"
        exit 1
    fi

    printf '%s\n' "${selected[@]}"
}

process_repo() {
    local repo="$1"
    local repo_name
    repo_name=$(basename "$repo")

    # Check if package.json exists and contains next
    local pkg_content
    if ! pkg_content=$(gh api "repos/$repo/contents/package.json" --jq '.content' 2>/dev/null | base64 -d 2>/dev/null); then
        return 1
    fi

    if ! echo "$pkg_content" | grep -q '"next"'; then
        return 1
    fi

    NEXTJS_REPOS+=("$repo")
    success "Found Next.js project: $repo"

    if [[ "$DRY_RUN" == "true" ]]; then
        log "[DRY RUN] Would scan and fix $repo"
        return 0
    fi

    # Clone if not already cloned (full clone for lockfile commits)
    if [[ ! -d "$repo_name" ]]; then
        log "Cloning $repo..."
        if ! gh repo clone "$repo" "$repo_name" 2>/dev/null; then
            error "Failed to clone $repo"
            FAILED_REPOS+=("$repo - clone failed")
            return 1
        fi
    fi

    cd "$repo_name"

    # Use official Vercel fix tool (handles monorepos, React RSC packages, lockfiles)
    log "Running fix-react2shell-next..."
    if npx --yes fix-react2shell-next@latest --fix 2>&1 | tee -a "$LOG_FILE"; then
        # Check if any changes were made
        if git diff --quiet HEAD 2>/dev/null; then
            success "Already patched"
            cd "$WORK_DIR"
            return 0
        fi

        # Commit changes (package.json + lockfiles, exclude node_modules)
        git add -A
        git reset HEAD -- node_modules 2>/dev/null || true

        if ! git commit -m "security: patch Next.js vulnerabilities

Applied via fix-react2shell-next (official Vercel tool)

CVE-2025-66478 (RCE), CVE-2025-55183 (Source Code Exposure)
CVE-2025-55184 (DoS), CVE-2025-67779 (Complete DoS Fix)

https://github.com/vercel-labs/fix-react2shell-next" 2>/dev/null; then
            success "No changes needed"
            cd "$WORK_DIR"
            return 0
        fi

        UPGRADED_REPOS+=("$repo")
        success "Patched $repo"

        if [[ "$AUTO_PUSH" == "true" ]]; then
            log "Pushing..."
            if git push 2>/dev/null; then
                success "Pushed"
            else
                warn "Push failed (may need manual push)"
            fi
        fi
    else
        warn "Fix tool reported issues for $repo (may already be patched)"
    fi

    cd "$WORK_DIR"
    return 0
}

main() {
    [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]] && usage

    check_dependencies

    # Get accounts
    local -a accounts=()
    if [[ $# -gt 0 ]]; then
        accounts=("$@")
    else
        while IFS= read -r account; do
            [[ -n "$account" ]] && accounts+=("$account")
        done < <(select_accounts)
    fi

    if [[ ${#accounts[@]} -eq 0 ]]; then
        error "No accounts specified"
        exit 1
    fi

    # Setup
    mkdir -p "$WORK_DIR"
    echo "Next.js Security Update Log - $(date)" > "$LOG_FILE"
    echo "Accounts: ${accounts[*]}" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"

    echo ""
    log "Work directory: $WORK_DIR"
    log "Scanning accounts: ${accounts[*]}"
    [[ "$DRY_RUN" == "true" ]] && warn "DRY RUN MODE - no changes will be made"
    [[ "$AUTO_PUSH" == "true" ]] && warn "AUTO PUSH ENABLED"

    cd "$WORK_DIR"

    declare -g -a REPOS=()
    declare -g -a NEXTJS_REPOS=()
    declare -g -a UPGRADED_REPOS=()
    declare -g -a FAILED_REPOS=()

    for account in "${accounts[@]}"; do
        log "Fetching repos from $account..."
        while IFS= read -r repo; do
            [[ -n "$repo" ]] && REPOS+=("$account/$repo")
        done < <(gh repo list "$account" --limit 500 --json name --jq '.[].name' 2>/dev/null || true)
    done

    log "Found ${#REPOS[@]} total repositories"

    for repo in "${REPOS[@]}"; do
        echo ""
        log "Checking $repo..."
        process_repo "$repo" || echo "  Not a Next.js project, skipping"
    done

    # Summary
    echo ""
    echo "=============================================="
    echo "           UPGRADE SUMMARY"
    echo "=============================================="
    echo ""
    echo "Total repos scanned: ${#REPOS[@]}"
    echo "Next.js projects found: ${#NEXTJS_REPOS[@]}"
    echo "Successfully upgraded: ${#UPGRADED_REPOS[@]}"
    echo "Failed: ${#FAILED_REPOS[@]}"
    echo ""

    if [[ ${#UPGRADED_REPOS[@]} -gt 0 ]]; then
        echo -e "${GREEN}Upgraded repos:${NC}"
        for r in "${UPGRADED_REPOS[@]}"; do
            echo "  - $r"
        done
        echo ""
        if [[ "$AUTO_PUSH" != "true" ]]; then
            echo -e "${YELLOW}To push all changes:${NC}"
            echo "  cd $WORK_DIR && for d in */; do (cd \"\$d\" && git push 2>/dev/null && echo \"Pushed \$d\"); done"
        fi
    fi

    if [[ ${#FAILED_REPOS[@]} -gt 0 ]]; then
        echo ""
        echo -e "${RED}Failed repos:${NC}"
        for r in "${FAILED_REPOS[@]}"; do
            echo "  - $r"
        done
    fi

    echo ""
    echo "Log saved to: $LOG_FILE"
}

main "$@"
