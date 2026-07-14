from pyaudio import PyAudio, paInt16

pya = PyAudio()

class audio:

    def __init__(self, **kwargs) -> None:
        self.stream = pya.open(
            format = paInt16,
            channels = 1,
            rate = 8000,
            **kwargs
        )

    def read(self, num_frames) -> bytes:
        # amodem's init sync loops can request 0 frames, which crashes PyAudio

        if num_frames <= 0:
            return b''

        try:
            # exception_on_overflow=False prevents crashes from radio squelch lags
            return self.stream.read(num_frames, exception_on_overflow=False)
        except Exception:
            return b''

    def __getattr__(self, name:str):
        return getattr(self.stream, name)

