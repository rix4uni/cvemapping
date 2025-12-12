# nextjs-security-update

There are people building OSS tools to exploit the new Next.js vulnerabilities. This is a tool to fight back - makes it dumb easy to upgrade all your Next.js apps across all your GitHub accounts.

Uses the [official Vercel fix tool](https://github.com/vercel-labs/fix-react2shell-next) under the hood.

## What happened

Dec 11, 2025: Next.js disclosed multiple critical vulnerabilities affecting React Server Components with App Router:
- CVE-2025-66478 (RCE)
- CVE-2025-55183 (Source Code Exposure)
- CVE-2025-55184 (DoS)
- CVE-2025-67779 (Complete DoS Fix)

https://nextjs.org/blog/cve-2025-55183-and-cve-2025-55184

## What this does

1. Discovers all your GitHub accounts (personal + orgs)
2. Lets you pick which ones to scan
3. Finds every Next.js repo
4. Runs the official Vercel fix tool on each (handles monorepos, React RSC packages, lockfiles)
5. Commits locally (you push when ready)

## Usage

```bash
curl -O https://raw.githubusercontent.com/williavs/nextjs-security-update/main/nextjs-security-update.sh
chmod +x nextjs-security-update.sh
./nextjs-security-update.sh
```

Or specify accounts directly:

```bash
./nextjs-security-update.sh myusername myorg
```

## Options

```bash
DRY_RUN=true ./nextjs-security-update.sh    # See what would change
AUTO_PUSH=true ./nextjs-security-update.sh  # Push automatically
```

## Requirements

- `gh` (GitHub CLI) - authenticated
- `node` / `npx`
- `git`

## After running

Push all changes:
```bash
cd ~/nextjs-security-updates
for d in */; do (cd "$d" && git push && echo "Pushed $d"); done
```

Then redeploy your apps.
