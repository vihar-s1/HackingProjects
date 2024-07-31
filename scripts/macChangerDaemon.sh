if [ "$(id -u)" -ne "0" ]; then
    echo "This script requires superuser privileges"
    exit -1
fi


macchanger_mac_daemon() {
    while true; do
        echo "Randomizing MAC Address..."
        new_mac=$(`openssl rand -hex 6 | sed 's/\(..\)/\1:/g; s/.$//'`)
        ifconfig $interface down
        ifconfig $interface hw ether $new_mac
        ifconfig $interface up
        sleep 60 # change MAC address every 60 seconds
    done
}


macchanger_linux_daemon() {
    while true; do
        echo "Randomizing MAC Address..."
        ifconfig $interface down
        macchanger -r $interface
        ifconfig $interface up
        sleep 60 # change MAC address every 60 seconds
    done
}


macchanger_daemon() {
    macchanger__mac_daemon &
    macchanger_pid=$!
    trap "kill $macchanger_pid" SIGINT SIGTERM
    wait $macchanger_pid
}



//---------- MAIN SCRIPT BEGINS HERE -----------//

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <interface>"
    exit -1
fi

interface=$1

// validating interface
ifconfig $interface > /dev/null 2>&1
if [ "$?" -ne "0" ]; then
    echo "Interface $interface not found"
    exit -1
fi

echo "Starting MAC Address randomization daemon for $interface..."
daemon_pid=""
if [ -f /usr/bin/macchanger ]; then
    macchanger_linux_daemon & > /dev/null 2>&1
    daemon_pid=$!
else
    macchanger_mac_daemon & > /dev/null 2>&1
    daemon_pid=$!
fi

echo "MAC Address randomization daemon started at PID $daemon_pid"
trap "kill $daemon_pid" SIGINT SIGTERM
echo "run 'kill $daemon_pid' to stop the daemon"