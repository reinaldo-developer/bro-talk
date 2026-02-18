from dataclasses import dataclass


@dataclass(frozen=True)
class AudioConfig:
    SAMPLE_RATE: int = 16000
    CHANNELS: int = 1
    CHUNK_SIZE: int = 320
    FORMAT: int = 8
    SILENCE_THRESHOLD_MS: int = 1000
    VAD_AGGRESSIVENESS: int = 3
    BEAM_SIZE: int = 5
    OUTPUT_SAMPLE_RATE: int = 22050


@dataclass(frozen=True)
class LLMConfig:
    MODEL: str = "llama3"
    TIMEOUT: int = 30
    STREAM: bool = True


@dataclass(frozen=True)
class TTSConfig:
    COMMAND: str = "espeak-ng"
    VOICE: str = "pt-br"
    SPEED: int = 160


@dataclass(frozen=True)
class AppConfig:
    EXIT_COMMAND: str = "sair"
    DEFAULT_LLM_MODEL: str = "llama3"
    DEFAULT_VOICE: str = "pt_BR-faber-medium"
    LANGUAGE: str = "pt"
