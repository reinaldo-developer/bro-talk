from dataclasses import dataclass


@dataclass(frozen=True)
class AudioConfig:
    SAMPLE_RATE: int = 16000
    CHANNELS: int = 1
    CHUNK_SIZE: int = 1024
    FORMAT: str = "float32"
    SILENCE_THRESHOLD: float = 0.01


@dataclass(frozen=True)
class AppConfig:
    EXIT_COMMAND: str = "sair"
    DEFAULT_LLM_MODEL: str = "llama3"
