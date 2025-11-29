#!/bin/bash


# Hardcoded Discord webhook URL
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/"

# Function to run the main logic
run_check() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running check..." >&2
  
  git clone https://github.com/rix4uni/cvemapping.git --depth 1

  # Check if cvemapping.txt exists before running (first run check)
  IS_FIRST_RUN=false
  if [ ! -f cvemapping.txt ]; then
    IS_FIRST_RUN=true
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] First run detected (cvemapping.txt not found)" >&2
  fi

  # Capture output from unew command
  OUTPUT=$(ls cvemapping/{2020,2021,2022,2023,2024,2025} \
    | egrep -v ":" \
    | awk -v base="https://github.com/rix4uni/cvemapping/tree/main" '
        {
          split($0, a, "-");
          year=a[2];
          print base "/" year "/" $0
        }
      ' \
    | unew cvemapping.txt)

  # Output to stdout (for compatibility with existing usage)
  echo "$OUTPUT"

  rm -rf cvemapping

  # Skip Discord notification on first run to avoid sending all output
  if [ "$IS_FIRST_RUN" = true ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Skipping Discord notification on first run" >&2
    return 0
  fi

  # Send to Discord if we have output and file exists
  if [ -n "$OUTPUT" ]; then
    # Wrap URLs in angle brackets to prevent Discord embeds (each line is a URL)
    DISCORD_OUTPUT=$(echo "$OUTPUT" | sed 's|^https://|<https://|g' | sed 's|$|>|g')
    
    # Build JSON payload with jq if available, otherwise use manual escaping
    if command -v jq >/dev/null 2>&1; then
      PAYLOAD=$(echo "$DISCORD_OUTPUT" | jq -Rs '{content: .}')
    else
      # Fallback: manually escape JSON
      ESCAPED_OUTPUT=$(echo "$DISCORD_OUTPUT" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')
      PAYLOAD="{\"content\": \"$ESCAPED_OUTPUT\"}"
    fi
    
    # Send to Discord webhook
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
      -H "Content-Type: application/json" \
      -d "$PAYLOAD" \
      "$DISCORD_WEBHOOK_URL")
    
    if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 204 ]; then
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Sent to Discord (HTTP $HTTP_CODE)" >&2
    else
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Failed to send to Discord (HTTP $HTTP_CODE)" >&2
    fi
  else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] No new directories found" >&2
  fi
}

# Run forever, every 3600 seconds (1 hour)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting cvemapping monitor (runs every 3600 seconds)..." >&2
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Press Ctrl+C to stop" >&2

while true; do
  run_check
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Waiting 3600 seconds until next check..." >&2
  sleep 3600
done
