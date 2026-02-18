import subprocess
from typing import Iterator
from src.interfaces.synthesizer import SynthesizerStrategy
from src.domain.config import TTSConfig


class EspeakTTS(SynthesizerStrategy):
    def synthesize(self, text_stream: Iterator[str]) -> Iterator[bytes]:
        buffer: list[str] = []
        sentence_enders = {".", "!", "?", "\n", ":", ";"}

        for token in text_stream:
            buffer.append(token)
            if any(ender in token for ender in sentence_enders):
                full_text = "".join(buffer)
                yield from self._generate_audio(full_text)
                buffer = []

        if buffer:
            yield from self._generate_audio("".join(buffer))

    def _generate_audio(self, text: str) -> Iterator[bytes]:
        if not text.strip():
            return

        process = subprocess.Popen(
            [
                TTSConfig.COMMAND,
                "-v",
                TTSConfig.VOICE,
                "-s",
                str(TTSConfig.SPEED),
                "--stdout",
                text,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )

        if process.stdout:
            while True:
                chunk = process.stdout.read(1024)
                if not chunk:
                    break
                yield chunk
