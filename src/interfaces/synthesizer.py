from abc import ABC, abstractmethod
from typing import Iterator


class SynthesizerStrategy(ABC):
    @abstractmethod
    def synthesize(self, text_stream: Iterator[str]) -> Iterator[bytes]:
        pass
