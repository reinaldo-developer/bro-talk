from typing import Iterator, Any
from src.interfaces.llm import LLMStrategy
from src.domain.config import LLMConfig


class OllamaLLM(LLMStrategy):
    def __init__(self, client: Any, model: str = LLMConfig.MODEL):
        self._client = client
        self._model = model

    def generate_response(self, prompt: str) -> Iterator[str]:
        response_stream = self._client.chat(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            stream=LLMConfig.STREAM,
        )

        for chunk in response_stream:
            content = chunk.get("message", {}).get("content", "")
            if content:
                yield content
