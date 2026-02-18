from io import BytesIO
from typing import Any
from src.interfaces.transcriber import TranscriberStrategy
from src.domain.config import AudioConfig, AppConfig


class WhisperTranscriber(TranscriberStrategy):
    def __init__(self, model: Any):
        self._model = model

    def transcribe(self, audio_data: bytes) -> str:
        audio_file = BytesIO(audio_data)
        segments, _ = self._model.transcribe(
            audio_file,
            beam_size=AudioConfig.BEAM_SIZE,
            language=AppConfig.LANGUAGE,
            vad_filter=True,
        )
        return " ".join([segment.text for segment in segments]).strip()
