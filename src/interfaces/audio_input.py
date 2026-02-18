from abc import ABC, abstractmethod
from typing import Iterator


class AudioInputStrategy(ABC):
    @abstractmethod
    def listen(self) -> Iterator[bytes]:
        pass

    @abstractmethod
    def start_stream(self) -> None:
        pass

    @abstractmethod
    def stop_stream(self) -> None:
        pass
