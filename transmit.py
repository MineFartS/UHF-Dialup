from amodem.config import bitrates
from amodem import audio
from amodem import main

interface = audio.Interface(bitrates[1])
interface.load(f"dll/libportaudio64bit.dll")

with interface:
        
    main.send(
        config = bitrates[1], 
        src = open("test.txt", 'rb'), 
        dst = interface.player(),
        gain = 1.0, 
        extra_silence = 0.0
    )
