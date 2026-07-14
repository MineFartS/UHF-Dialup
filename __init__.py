from amodem.config import Configuration
import os, struct, fcntl, pyaudio
from functools import partial

audio = partial(
    pyaudio.PyAudio().open,
    format = pyaudio.paInt16,
    channels = 1,
    rate = 8000
)


cfg = Configuration()
cfg.f_min = 600      # Low end of typical radio audio passband
cfg.f_max = 2800     # High end of radio audio passband
cfg.f_carrier = 1700 # Center frequency



# Open and bind the Linux virtual TUN device
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack("16sH", b"tun0", 0x0001|0x1000)
fcntl.ioctl(tun, 0x400454ca, ifr)

tunnel = lambda m: os.fdopen(os.dup(tun), m)

