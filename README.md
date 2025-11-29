## cvemapping

This repo Gathers all available cve exploits from github.

## Installation
```
go install github.com/rix4uni/cvemapping@latest
```

## Download prebuilt binaries
```
wget https://github.com/rix4uni/cvemapping/releases/download/v0.0.1/cvemapping-linux-amd64-0.0.1.tgz
tar -xvzf cvemapping-linux-amd64-0.0.1.tgz
rm -rf cvemapping-linux-amd64-0.0.1.tgz
mv cvemapping ~/go/bin/cvemapping
```
Or download [binary release](https://github.com/rix4uni/cvemapping/releases) for your platform.

## Compile from source
```
git clone --depth 1 github.com/rix4uni/cvemapping.git
cd cvemapping; go install
```

## Usage
```yaml
Usage of cvemapping:
  -github-token string
        GitHub Token for authentication
  -page string
        Page number to fetch, or 'all' (default "1")
  -year string
        Year to search for CVEs (e.g., 2024, 2020)
```

## Usage Examples
```yaml
echo '"CVE-2024-"' | cvemapping -github-token "TOKEN" -page all -year 2024
```

**Note:** This repository also includes an automated GitHub Actions workflow that runs hourly. For manual usage, see the examples above.

## Automated Workflow

This repository uses GitHub Actions to automatically:
- Scan GitHub for new CVE exploits every hour
- Monitor CVEs from years 2020-2025
- Clone and organize repositories by CVE ID
- Send Discord notifications when new CVE directories are created
- Commit and push updates to the repository

The workflow runs:
- **Scheduled:** Every hour (cron: `0 * * * *`)
- **On push:** When changes are pushed to the `main` branch

### Monitored Years
The automated workflow currently monitors:
- 2025
- 2024
- 2023
- 2022
- 2021
- 2020

## Discord Notifications

When the automated workflow creates new CVE directories, it sends batched Discord notifications with links to each new directory. The notification format is:

```
NEW ALERT: https://github.com/rix4uni/cvemapping/tree/main/{year}/{cve-name}
```

All new directories from a single workflow run are batched into one Discord message.

### Features
- **Automatic tracking:** New directories are tracked as soon as they're created
- **Batched notifications:** All new directories from one run are sent in a single message
- **Comprehensive coverage:** Tracks all new directories, even if they're later deleted due to size/file count limits

## Configuration

### Setting up Discord Webhook

To enable Discord notifications, you need to add your Discord webhook URL to GitHub secrets:

1. Create a Discord webhook:
   - Go to your Discord server settings
   - Navigate to Integrations → Webhooks
   - Create a new webhook and copy the webhook URL

2. Add the webhook URL to GitHub:
   - Go to `https://github.com/rix4uni/cvemapping/settings/environments`
   - Or navigate to: Repository Settings → Secrets and variables → Actions
   - Add a new secret named `DISCORD_WEBHOOK_URL`
   - Paste your Discord webhook URL as the value

3. The workflow will automatically use this secret when sending notifications.

**Note:** If `DISCORD_WEBHOOK_URL` is not set, the workflow will skip sending notifications but continue running normally.
