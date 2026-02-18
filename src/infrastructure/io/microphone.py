import pyaudio
from pyaudio import Stream
from typing import Iterator, List
from src.interfaces.audio_input import AudioInputStrategy
from src.interfaces.vad import VADStrategy
from src.domain.config import AudioConfig


class MicrophoneInput(AudioInputStrategy):
    def __init__(
        self, vad_strategy: VADStrategy, input_device_index: int | None = None
    ):
        self._audio_interface = pyaudio.PyAudio()
        self._input_device_index = input_device_index
        self._stream: Stream | None = None
        self._vad_strategy = vad_strategy
        self._is_listening = False
        self._frames: List[bytes] = []

    def start_stream(self) -> None:
        self._stream = self._audio_interface.open(
            format=AudioConfig.FORMAT,
            channels=AudioConfig.CHANNELS,
            rate=AudioConfig.SAMPLE_RATE,
            input=True,
            frames_per_buffer=AudioConfig.CHUNK_SIZE,
            input_device_index=self._input_device_index,
        )
        self._is_listening = True

    def stop_stream(self) -> None:
        self._is_listening = False
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None
        self._audio_interface.terminate()

    def listen(self) -> Iterator[bytes]:
        silence_counter = 0
        frames_per_second = AudioConfig.SAMPLE_RATE / AudioConfig.CHUNK_SIZE
        silence_threshold_frames = int(
            (AudioConfig.SILENCE_THRESHOLD_MS / 1000) * frames_per_second
        )
        has_speech_started = False

        if not self._stream or not self._stream.is_active():
            self.start_stream()

        assert self._stream is not None

        while self._is_listening:
            try:
                chunk = self._stream.read(
                    AudioConfig.CHUNK_SIZE, exception_on_overflow=False
                )
                is_speech = self._vad_strategy.is_speech(chunk, AudioConfig.SAMPLE_RATE)

                if is_speech:
                    has_speech_started = True
                    silence_counter = 0
                    self._frames.append(chunk)

                elif has_speech_started:
                    silence_counter += 1
                    self._frames.append(chunk)

                    if silence_counter >= silence_threshold_frames:
                        yield b"".join(self._frames[:-silence_threshold_frames])
                        self._frames = []
                        has_speech_started = False
                        silence_counter = 0

            except OSError:
                break
