#=====================================================================
# Modem
from amodem.config import Configuration
from amodem.recv import Receiver
from amodem import main

cfg = Configuration()
cfg.f_min = 600      # Low end of typical radio audio passband
cfg.f_max = 2800     # High end of radio audio passband
cfg.f_carrier = 1700 # Center frequency
cfg.timeout = 99999.0        # Force amodem stream.py to wait indefinitely for bytes
cfg.silence_start = 0.0      # Disable strict pre-carrier silence checks
cfg.skip_start = 0.0         # Prevent skipping the initial audio frame blocks

class _modem(Receiver):
    
    def recv(self, src, dst):
        while True:
            try:
                super().run(
                    sampler = src,
                    output = dst,
                    gain = 1.0
                )
            except OSError as e:
                if 'timeout' in str(e):
                    continue
                else:
                    raise e

    def send(self, src, dst) -> None:
        main.send(
            config = cfg, 
            src = src, 
            dst = dst
        )

modem = _modem(config=cfg)

#=====================================================================
# Tunnel
import os, sys, fcntl, struct

def tunnel(mode:str):

    if not hasattr(sys, '_tun_fd'):    
        # Open and bind the Linux virtual TUN device exactly ONCE globally
        sys._tun_fd = os.open("/dev/net/tun", os.O_RDWR)
        ifr = struct.pack("16sH", b"tun0", 0x0001|0x1000)
        fcntl.ioctl(sys._tun_fd, 0x400454ca, ifr)

    return os.fdopen(os.dup(sys._tun_fd), mode)

#=====================================================================
# Audio
from pyaudio import PyAudio, paInt16
import numpy as np

pya = PyAudio()

class audio:

    def __init__(self, **kwargs) -> None:
        self.stream = pya.open(
            format = paInt16,
            channels = 1,
            rate = 8000,
            **kwargs
        )
        
    def take(self, size):
        if size <= 0:
            return np.zeros(0, dtype=np.float32)
        try:
            # Read raw 16-bit PCM binary data from the microphone
            raw_data = self.stream.read(size, exception_on_overflow=False)
            
            # Convert binary string into a numeric 1D numpy array
            samples = np.frombuffer(raw_data, dtype=np.int16)
            
            # Normalize integers into a float range (-1.0 to 1.0) expected by amodem
            return samples.astype(np.float32) / 32768.0
            
        except Exception:
            # If a radio static glitch or hardware error occurs, feed silence to maintain timing
            return np.zeros(size, dtype=np.float32)

    def __getattr__(self, name:str):
        return getattr(self.stream, name)

#=====================================================================

