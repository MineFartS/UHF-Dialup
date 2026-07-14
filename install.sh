
#===============================================
# Dependencies

# Install Python
sudo apt install -y python3
sudo apt install -y python3-pip
sudo apt install -y python3-venv

# Create & Activate Python Venv
python3 -m venv .venv
source .venv/bin/activate

# Install Required Python Packages
python3 -m pip install -r requirements.txt

# Install PortAudio
sudo apt install -y portaudio19-dev
sudo apt install -y libportaudio2

#===============================================
# Network Tunnel

# Create a virtual TUN interface named tun0
sudo ip tuntap add dev tun0 mode tun

# Assign an IP to Device A
sudo ip addr add 10.0.0.1/24 dev tun0  # (On Device B, use 10.0.0.2/24)

# Bring the interface up
sudo ip link set dev tun0 up

# Grant Python Network Capabilities
sudo setcap cap_net_admin+ep "$(readlink -f .venv/bin/python3)"

#===============================================
