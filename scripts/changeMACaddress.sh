#!/bin/bash

# MAC Address Changer Script
# Changes MAC address to a random value or a specified one

if [ "$(id -u)" != "0" ]; then
    echo "Error: This script requires superuser privileges"
    exit 1
fi

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <interface> [newMAC]"
    echo "  interface  - Network interface (e.g., eth0, wlan0)"
    echo "  newMAC     - Optional: specific MAC address or 'random'"
    exit 1
fi

interface="$1"
newMAC=""

# Validate interface exists
if ! ip link show "$interface" > /dev/null 2>&1; then
    echo "Error: Interface '$interface' not found"
    exit 1
fi

# Get original MAC address for restoration on failure
original_mac=$(ip link show "$interface" | awk '/link\/ether/ {print $2}')

if [ "$#" -eq 2 ]; then
    newMAC="$2"
fi

# Function to restore original MAC on failure
restore_mac() {
    if [ -n "$original_mac" ]; then
        ip link set "$interface" down
        ip link set "$interface" address "$original_mac"
        ip link set "$interface" up
        echo "Original MAC address restored: $original_mac"
    fi
}

# Set trap to restore MAC on script termination
trap restore_mac ERR INT TERM

# Bring interface down
if ! ip link set "$interface" down; then
    echo "Error: Failed to bring interface '$interface' down"
    exit 1
fi

if [ -z "$newMAC" ] || [ "$newMAC" = "random" ]; then
    echo "Randomizing MAC Address..."
    if command -v macchanger > /dev/null 2>&1; then
        if ! macchanger -r "$interface"; then
            echo "Error: macchanger failed"
            restore_mac
            exit 1
        fi
    else
        # Generate random MAC using openssl or fallback
        if command -v openssl > /dev/null 2>&1; then
            newMAC=$(openssl rand -hex 6 | sed 's/\(..\)/\1:/g; s/.$//')
        else
            # Fallback without openssl
            newMAC=$(printf '%02X:%02X:%02X:%02X:%02X:%02X' $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)))
        fi
        if ! ip link set "$interface" address "$newMAC"; then
            echo "Error: Failed to set MAC address to $newMAC"
            restore_mac
            exit 1
        fi
    fi
else
    echo "Changing MAC Address to $newMAC..."
    if command -v macchanger > /dev/null 2>&1; then
        if ! macchanger -m "$newMAC" "$interface"; then
            echo "Error: macchanger failed"
            restore_mac
            exit 1
        fi
    else
        if ! ip link set "$interface" address "$newMAC"; then
            echo "Error: Failed to set MAC address to $newMAC"
            restore_mac
            exit 1
        fi
    fi
fi

# Bring interface up
if ! ip link set "$interface" up; then
    echo "Error: Failed to bring interface '$interface' up"
    restore_mac
    exit 1
fi

# Display new MAC address
new_mac=$(ip link show "$interface" | awk '/link\/ether/ {print $2}')
echo "Success! MAC address changed to: $new_mac"

# Clear trap on successful completion
trap - ERR INT TERM
