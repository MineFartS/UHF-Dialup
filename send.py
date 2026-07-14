from __init__ import tunnel, modem, audio

modem.send(
    src = tunnel('rb'),
    dst = audio(output=True)
)

