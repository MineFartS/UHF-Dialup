from __init__ import tunnel, cfg
from audio import audio
from amodem import main

with tunnel('wb') as tun_stream:
    main.recv(
        config = cfg,
        src = audio(input=True),
        dst = tun_stream
    )

