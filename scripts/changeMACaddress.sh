if [ "$(id -u)" != "0" ]; then
    echo "This script requires superuser privileges"
    exit -1
fi

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <interface> [newMAC]"
    exit -1
fi

interface=$1
newMAC=null
if [ "$#" -eq 2 ]; then
    newMAC=$2
fi

ifconfig $interface down
if [ "$newMAC" == "null" ]; then
    echo "Randomizing MAC Address..."
    macchanger -r $interface
else
    echo "Changing MAC Address to $newMAC..."
    macchanger -m $newMAC $interface
fi
ifconfig $interface up