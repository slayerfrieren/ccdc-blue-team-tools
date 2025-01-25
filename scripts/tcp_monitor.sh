#!/bin/bash

# Define log file location
LOG_FILE="/var/log/tcp_monitor.log"

# Define threshold for incomplete connections
THRESHOLD=10

# Get current timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Count TCP connections in SYN_RECV state
SYN_COUNT=$(netstat -an | grep 'SYN_RECV' | wc -l)

# Check if the count exceeds the threshold
if [ "$SYN_COUNT" -ge "$THRESHOLD" ]; then
    echo "$TIMESTAMP - ALERT: $SYN_COUNT incomplete TCP connections detected." >> "$LOG_FILE"
fi

# Maintain permissions on the log file
chmod 640 "$LOG_FILE"