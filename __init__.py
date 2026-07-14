from amodem.config import bitrates
from amodem.audio import Interface

config = bitrates[1]

iface = Interface(config)
iface.load("libportaudio.so.2")
