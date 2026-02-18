import pyaudio
from typing import Iterator
from src.interfaces.audio_output import AudioOutputStrategy
from src.domain.config import AudioConfig


class PyAudioSpeaker(AudioOutputStrategy):
    def __init__(self) -> None:
        self._audio_interface = pyaudio.PyAudio()
        self._stream: pyaudio.Stream | None = None

    def _open_stream(self) -> None:
        if self._stream is None:
            self._stream = self._audio_interface.open(
                format=AudioConfig.FORMAT,
                channels=AudioConfig.CHANNELS,
                rate=AudioConfig.OUTPUT_SAMPLE_RATE,
                output=True,
            )

    def play_stream(self, audio_stream: Iterator[bytes]) -> None:
        self._open_stream()
        assert self._stream is not None

        try:
            for chunk in audio_stream:
                if chunk:
                    self._stream.write(chunk)
        finally:
            self._close_stream()

    def _close_stream(self) -> None:
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None

    def __del__(self) -> None:
        self._audio_interface.terminate()
