#!/bin/bash

# --- PERSISTENT ROOT ENFORCEMENT ---
if [ "$EUID" -ne 0 ]; then
  echo "Please execute this network script with sudo privileges (sudo bash start.sh)."
  exit 1
fi

LOCAL_IP="10.0.0.$1"
REMOTE_IP="10.0.0.$2"

echo "=== PHASE 1: INITIALIZING VIRTUAL COM PIPELINE ==="
bash ./tty0tty/start.sh
if [ $? -ne 0 ]; then
  echo "[X] Critical error during tty0tty instantiation."
  exit 1
fi

echo "=== PHASE 2: SPAWNING DIREWOLF PACKET MODEM ==="
if [ ! -f ./direwolf/bin/direwolf ]; then
  echo "[*] Compiling direwolf inside untracked directory..."
  cd direwolf && make && cd ..
fi

# Wipe old logs to keep diagnostics clear
rm -f /var/log/direwolf_network.log

bash ./direwolf/run.sh -c ./direwolf.conf > /var/log/direwolf_network.log 2>&1 &
DIREWOLF_PID=$!
echo $DIREWOLF_PID > /tmp/direwolf_net.pid

# Verify background stabilization
sleep 2
if ! kill -0 $DIREWOLF_PID 2>/dev/null; then
  echo "[X] Critical: Direwolf closed immediately after launching!"
  echo "--- LAST ERROR LOGS ---"
  cat /var/log/direwolf_network.log
  echo "-----------------------"
  exit 1
fi
echo "[✓] Direwolf wrapper initialized background daemon (PID: $DIREWOLF_PID)"

echo "=== PHASE 3: BINDING LINUX TNC INTERFACE ==="
# Cushion time for Direwolf to successfully lock onto /dev/tnt0
sleep 1.5

# Compile tncattach from source if its binary is absent
if [ ! -f ./tncattach/tncattach ]; then
  echo "[*] tncattach binary missing. Compiling from untracked source..."
  cd tncattach && make && cd ..
fi

# Hardcode interface target cleanly to bypass dynamic loop issues
IFACE="tnc0"

# Map interfaces using your specialized tncattach wrapper execution syn
echo "Configuring Point-to-Point pipeline mapping..."

# Invoke wrapper in the background explicitly to safeguard against foreground lockups
bash ./tncattach/run.sh /dev/tnt1 115200 -d --noipv6 --noup --mtu 496 > /var/log/tncattach_network.log 2>&1 &
sleep 1.0

if ip link show tnc1 &>/dev/null; then IFACE="tnc1"; fi

# Inject the dynamically determined IP endpoints mapped to this Node ID
ip addr add "$LOCAL_IP" peer "$REMOTE_IP" dev "$IFACE" 2>/dev/null || true
ip link set dev "$IFACE" up
echo "[✓] Network routing active: $IFACE bound to local $LOCAL_IP -> peer $REMOTE_IP"

echo "=== INFRASTRUCTURE INITIALIZATION COMPLETE ==="
