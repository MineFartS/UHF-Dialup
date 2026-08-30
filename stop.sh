#!/bin/bash
if [ "$EUID" -ne 0 ]; then
  echo "Please execute teardown with sudo privileges (sudo bash stop.sh)."
  exit 1
fi

echo "=== TEARING DOWN IP-OVER-AX25 PIPELINE ==="

# 1. Kill the network link adapter and physically remove the link node descriptor
if pgrep -f tncattach > /dev/null; then
  echo "Bringing down tncattach instances..."
  pkill -f tncattach
fi

if ip link show tnc0 &>/dev/null; then
  echo "Flushing and deleting virtual adapter tnc0..."
  ip link set dev tnc0 down 2>/dev/null || true
  ip link delete dev tnc0 2>/dev/null || true
fi

# 2. Terminate the packet modem process spawned by your wrapper
if [ -f /tmp/direwolf_net.pid ]; then
  echo "Stopping Direwolf background process..."
  kill $(cat /tmp/direwolf_net.pid) 2>/dev/null
  rm /tmp/direwolf_net.pid
else
  pkill -f direwolf
fi

# 3. Offload module teardown to your localized tty0tty stop wrapper explicitly using bash
bash ./tty0tty/stop.sh clean

echo "[✓] Network stack completely isolated and cleaned."
