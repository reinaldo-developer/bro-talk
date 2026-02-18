from abc import ABC, abstractmethod


class TranscriberStrategy(ABC):
    @abstractmethod
    def transcribe(self, audio_data: bytes) -> str:
        pass
