from abc import ABC, abstractmethod


class VADStrategy(ABC):
    @abstractmethod
    def is_speech(self, frame: bytes, sample_rate: int) -> bool:
        pass
