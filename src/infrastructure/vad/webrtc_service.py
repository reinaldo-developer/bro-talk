import webrtcvad
from src.interfaces.vad import VADStrategy
from src.domain.config import AudioConfig


class WebRTCVAD(VADStrategy):
    def __init__(self):
        self._model = webrtcvad.Vad(AudioConfig.VAD_AGGRESSIVENESS)

    def is_speech(self, frame: bytes, sample_rate: int) -> bool:
        return self._model.is_speech(frame, sample_rate)