from __init__ import iface, config
from amodem import main

with iface:
        
    main.recv(
        config = config, 
        src = iface.recorder(), 
        dst = open("recv.txt", 'wb')
    )
