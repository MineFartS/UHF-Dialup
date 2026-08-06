#===============================================
# Dependencies

# Install Python & System Dev Libraries

sudo apt update
sudo apt install -y git
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y portaudio19-dev libportaudio2

# Create Python Venv (if it doesn't exist)
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Upgrade pip inside the venv
.venv/bin/pip install --upgrade pip

# Install Required Python Packages directly using the venv binary
.venv/bin/pip install -r requirements.txt

#===============================================
# Network Tunnel

# Create a virtual TUN interface named tun0
sudo ip tuntap add dev tun0 mode tun

# Assign an IP to Device A
sudo ip addr add 10.0.0.1/24 dev tun0

# Bring the interface up
sudo ip link set dev tun0 up

# Grant the specific Venv Python binary Network Capabilities
sudo setcap cap_net_admin+ep "$(readlink -f .venv/bin/python3)"

#===============================================

source .venv/bin/activate
