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

# Brief pause to let Direwolf spin up the virtual device entries
sleep 2

# SYSTEM ADJUSTMENT: Automatically reduce audio capture gain to eliminate clipping
echo "[*] Normalizing audio card input mixer level..."
amixer -c "$3" sset Capture 25% >/dev/null 2>&1 || true

echo "=== PHASE 3: BINDING LINUX TNC INTERFACE ==="
echo "Configuring Serial Link KISS mapping..."

# FIXED: Removed the invalid '--tun' flag so tncattach initializes natively in point-to-point mode
bash ./tncattach/run.sh "/dev/tnt1" 115200 \
    -d \
    --noipv6 \
    -m 496 \
    -s "N0CALL" \
    -t 600 \
    > /var/log/tncattach_network.log 2>&1 &

echo "[*] Waiting for tncattach to generate $NET_IFACE device entry..."
FOR_LOOPS=0
while ! ip link show "$NET_IFACE" &>/dev/null; do
  sleep 0.5
  ((FOR_LOOPS++))
  if [ "$FOR_LOOPS" -gt 10 ]; then
    echo "[-] ERROR: tncattach failed to create $NET_IFACE interface within 5 seconds."
    echo "Checking /var/log/tncattach_network.log for details:"
    tail -n 5 /var/log/tncattach_network.log
    exit 1
  fi
done

# BIND NETWORKING LAYER: Inject the precise point-to-point endpoints
ip addr flush dev "$NET_IFACE" 2>/dev/null || true
ip addr add "$LOCAL_IP" peer "$REMOTE_IP" dev "$NET_IFACE"

# Configures interface features for modern iproute2 compatibility
ip link set dev $NET_IFACE arp off
ip link set dev $NET_IFACE up

# CRITICAL FILTER FIX: Explicitly drop background system multicast traffic (e.g., mDNS/Avahi)
# This completely eliminates the "Not AX.25" and "Invalid KISS frame length 6" logging errors.
sudo iptables -A OUTPUT -o $NET_IFACE -d 224.0.0.0/4 -j DROP
sudo iptables -A INPUT  -i $NET_IFACE -j ACCEPT
sudo iptables -A OUTPUT -o $NET_IFACE -j ACCEPT

echo "[✓] Network routing active: $NET_IFACE bound to local $LOCAL_IP -> peer $REMOTE_IP"
echo "=== INFRASTRUCTURE INITIALIZATION COMPLETE ==="
