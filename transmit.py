import logging
import os

from amodem import async_reader
from amodem import audio
from amodem import calib
from amodem import main
from amodem.config import bitrates

def FileType(mode, interface_factory=None):
    def opener(fname):
        audio_interface = interface_factory() if interface_factory else None

        assert 'r' in mode or 'w' in mode
        if audio_interface is None and fname is None:
            fname = '-'

        if fname is None:
            assert audio_interface is not None
            if 'r' in mode:
                s = audio_interface.recorder()
                return async_reader.AsyncReader(stream=s, bufsize=s.bufsize)
            if 'w' in mode:
                return audio_interface.player()

        if fname == '-':
            if 'r' in mode:
                return _stdin
            if 'w' in mode:
                return _stdout

        return open(fname, mode)

    return opener

def interface_factory():
        return interface

def wrap(cls, stream, enable):
    return cls(stream) if enable else stream

log = logging.getLogger('__name__')

bitrate = os.environ.get('BITRATE', 1)
config = bitrates.get(int(bitrate))

interface = audio.Interface(config)
audio_library = r"C:\Users\administrator.PHILH\Documents\GitHub\UHF Dialup\dll\libportaudio64bit.dll"
interface.load(audio_library)

#src = wrap(Compressor, FileType('rb')("test.csv"), False)
src = FileType('rb')("_kiss.py")
dst = FileType('wb', interface_factory)

#dst = FileType('wb', interface_factory)(None)
#dst = FileType('wb', interface_factory)('test.pcm')

main.send(config, src, dst, gain=1.0, extra_silence=0.0)