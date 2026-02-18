from abc import ABC, abstractmethod
from typing import Iterator


class AudioOutputStrategy(ABC):
    @abstractmethod
    def play_stream(self, audio_stream: Iterator[bytes]) -> None:
        pass
