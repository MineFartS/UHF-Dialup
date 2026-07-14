
# Install Python
sudo apt install -y python3
sudo apt install -y python3-pip
sudo apt install -y python3-venv

# Create & Activate Python Venv
python3 -m venv .venv
source .venv/bin/activate

# Install Required Python Packages
python3 -m pip install -r requirements.txt
