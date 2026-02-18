from abc import ABC, abstractmethod
from typing import Iterator


class LLMStrategy(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> Iterator[str]:
        pass
