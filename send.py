from __init__ import tunnel, cfg, audio
from amodem import main

with tunnel('rb') as tun_stream:
    main.send(
        config = cfg, 
        src = tun_stream,
        dst = audio(output=True)
    )

