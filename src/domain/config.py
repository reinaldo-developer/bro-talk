from dataclasses import dataclass


@dataclass(frozen=True)
class AudioConfig:
    SAMPLE_RATE: int = 16000
    CHANNELS: int = 1
    CHUNK_SIZE: int = 320
    FORMAT: int = 8
    SILENCE_THRESHOLD_MS: int = 1000
    VAD_AGGRESSIVENESS: int = 3


@dataclass(frozen=True)
class AppConfig:
    EXIT_COMMAND: str = "sair"
    DEFAULT_LLM_MODEL: str = "llama3"
    DEFAULT_VOICE: str = "pt_BR-faber-medium"