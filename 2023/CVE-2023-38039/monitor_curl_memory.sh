#!/bin/bash

# Function to clean up background processes
cleanup() {
    kill $EXPLOIT_SERVER_PID
    exit
}

# Trap the exit signal to ensure cleanup
trap cleanup EXIT

# Start the exploit server in the background
python3 exploit_server.py &
EXPLOIT_SERVER_PID=$!

# Allow the server to start
sleep 2

# Run curl and capture its PID
curl http://localhost:8080 &
CURL_PID=$!

# Allow some time for curl to start
sleep 1

# Check if the curl process is running and monitor its memory usage
if ps -p $CURL_PID > /dev/null; then
    echo "Monitoring curl (PID: $CURL_PID) memory usage..."
    while ps -p $CURL_PID > /dev/null; do
        ps -o pid,rss,vsize,comm -p $CURL_PID
        sleep 1
    done
else
    echo "Curl process not found"
fi

# Wait for the curl process to complete
wait $CURL_PID

# Cleanup
kill $EXPLOIT_SERVER_PID