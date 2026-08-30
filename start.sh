#!/bin/bash

# --- PERSISTENT ROOT ENFORCEMENT ---
if [ "$EUID" -ne 0 ]; then
  echo "Please execute this network script with sudo privileges (sudo bash start.sh)."
  exit 1
fi

# Ensure all runtime arguments exist before starting
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  echo "Usage: sudo bash start.sh <local_octet> <remote_octet> <audio_card_index>"
  echo "Example: sudo bash start.sh 1 2 3"
  exit 1
fi

LOCAL_IP="10.0.0.$1"
REMOTE_IP="10.0.0.$2"
AUDIO_IFACE="plughw:$3,0"
NET_IFACE="tnc0"

# Aggressively flush existing states to clear the port tables
bash stop.sh

echo "=== PHASE 1: INITIALIZING VIRTUAL COM PIPELINE ==="
bash ./tty0tty/start.sh

echo "=== PHASE 2: SPAWNING DIREWOLF PACKET MODEM ==="

cp ./direwolf.conf ./direwolf-temp.conf -f

# Dynamically match Direwolf config rules to command line parameters
echo "[*] Dynamically updating configuration to target: ADEVICE $AUDIO_IFACE"
sed -i "s|^ADEVICE.*|ADEVICE $AUDIO_IFACE|g" ./direwolf-temp.conf

bash ./direwolf/run.sh -c ./direwolf-temp.conf > /var/log/direwolf_network.log 2>&1 &
echo "[✓] Direwolf wrapper initialized background daemon (PID: $!)"

echo "=== PHASE 3: BINDING LINUX TNC INTERFACE ==="

echo "Configuring Point-to-Point pipeline mapping..."
bash ./tncattach/run.sh "/dev/tnt1" 115200 -d --noipv6 --mtu 496 > /var/log/tncattach_network.log 2>&1 &

# BIND NETWORKING LAYER: Inject the precise point-to-point endpoints
ip addr flush dev "$NET_IFACE" 2>/dev/null || true
ip addr add "$LOCAL_IP" peer "$REMOTE_IP" dev "$NET_IFACE"
ip link set dev "$NET_IFACE" up

echo "[✓] Network routing active: $NET_IFACE bound to local $LOCAL_IP -> peer $REMOTE_IP"
echo "=== INFRASTRUCTURE INITIALIZATION COMPLETE ==="
