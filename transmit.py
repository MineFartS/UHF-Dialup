from __init__ import iface, config
from amodem import main

with iface:
        
    main.send(
        config = config, 
        src = open("test.txt", 'rb'), 
        dst = iface.player(),
        gain = 1.0, 
        extra_silence = 0.0
    )
