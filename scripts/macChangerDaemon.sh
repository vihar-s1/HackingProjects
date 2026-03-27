#!/bin/bash

# MAC Address Changer Daemon
# Continuously randomizes MAC address at specified intervals

DAEMON_INTERVAL=60  # seconds between MAC changes

if [ "$(id -u)" -ne "0" ]; then
    echo "Error: This script requires superuser privileges"
    exit 1
fi

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <interface> [interval_seconds]"
    echo "  interface         - Network interface (e.g., eth0, wlan0)"
    echo "  interval_seconds  - Optional: interval between changes (default: 60)"
    exit 1
fi

interface="$1"

# Validate interface exists
if ! ip link show "$interface" > /dev/null 2>&1; then
    echo "Error: Interface '$interface' not found"
    exit 1
fi

# Optional custom interval
if [ "$#" -ge 2 ]; then
    if [[ "$2" =~ ^[0-9]+$ ]] && [ "$2" -gt 0 ]; then
        DAEMON_INTERVAL="$2"
    else
        echo "Warning: Invalid interval '$2', using default ($DAEMON_INTERVAL seconds)"
    fi
fi

# Store original MAC for cleanup
original_mac=$(ip link show "$interface" | awk '/link\/ether/ {print $2}')

# Cleanup function
cleanup() {
    echo ""
    echo "Stopping daemon..."
    if [ -n "$daemon_pid" ] && kill -0 "$daemon_pid" 2>/dev/null; then
        kill "$daemon_pid"
        wait "$daemon_pid" 2>/dev/null
    fi
    # Restore original MAC
    if [ -n "$original_mac" ]; then
        ip link set "$interface" down 2>/dev/null
        ip link set "$interface" address "$original_mac" 2>/dev/null
        ip link set "$interface" up 2>/dev/null
        echo "Original MAC address restored: $original_mac"
    fi
    echo "Daemon stopped."
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM EXIT

# Randomize MAC using macchanger
randomize_mac_macchanger() {
    ip link set "$interface" down
    if macchanger -r "$interface" > /dev/null 2>&1; then
        ip link set "$interface" up
        local new_mac=$(ip link show "$interface" | awk '/link\/ether/ {print $2}')
        echo "MAC address changed to: $new_mac"
    else
        echo "Error: macchanger failed"
        return 1
    fi
}

# Randomize MAC using openssl (macOS fallback)
randomize_mac_manual() {
    ip link set "$interface" down
    local new_mac=$(openssl rand -hex 6 | sed 's/\(..\)/\1:/g; s/.$//')
    if ip link set "$interface" address "$new_mac" 2>/dev/null; then
        ip link set "$interface" up
        echo "MAC address changed to: $new_mac"
    else
        echo "Error: Failed to set MAC address"
        return 1
    fi
}

# Main daemon loop
daemon_loop() {
    local randomize_func
    
    # Determine which method to use
    if command -v macchanger > /dev/null 2>&1; then
        randomize_func="randomize_mac_macchanger"
        echo "Using macchanger for MAC randomization"
    elif command -v openssl > /dev/null 2>&1; then
        randomize_func="randomize_mac_manual"
        echo "Using openssl for MAC randomization (manual method)"
    else
        echo "Error: Neither macchanger nor openssl found"
        exit 1
    fi
    
    echo "Starting MAC address randomization daemon for '$interface'"
    echo "Interval: $DAEMON_INTERVAL seconds"
    echo "Press Ctrl+C to stop"
    echo "-------------------------------------------"
    
    while true; do
        if ! $randomize_func; then
            echo "Warning: MAC randomization failed, retrying in $DAEMON_INTERVAL seconds..."
        fi
        sleep "$DAEMON_INTERVAL"
    done
}

# Start daemon in background
daemon_loop &
daemon_pid=$!

echo "Daemon started with PID: $daemon_pid"
echo "Press Ctrl+C to stop"

# Wait for daemon
wait "$daemon_pid"
