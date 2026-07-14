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

def tunnel(mode:str):

    # Open and bind the Linux virtual TUN device
    tun = os.open("/dev/net/tun", os.O_RDWR)

    ifr = struct.pack("16sH", b"tun0", 0x0001|0x1000)

    fcntl.ioctl(tun, 0x400454ca, ifr)

    return os.fdopen(tun, mode)

