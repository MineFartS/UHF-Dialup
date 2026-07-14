from __init__ import tunnel, modem, audio

modem.recv(
    src = audio(input=True),
    dst = tunnel('wb')
)
