from __init__ import tunnel, cfg, audio
from amodem import main

with tunnel('wb') as tun_stream:
    main.send(
        config = cfg,
        src = audio(input=True),
        dst = tun_stream
    )

