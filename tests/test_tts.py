import pytest
from unittest.mock import MagicMock, patch
from src.infrastructure.tts.espeak_service import EspeakTTS
from src.domain.config import TTSConfig


@pytest.fixture
def mock_subprocess():
    with patch("src.infrastructure.tts.espeak_service.subprocess.Popen") as mock:
        yield mock


def test_synthesize_buffers_text_until_punctuation(mock_subprocess):
    tts = EspeakTTS()
    input_text = iter(["Olá", " ", "mundo", ".", " ", "Teste"])
    
    mock_process = MagicMock()
    mock_process.stdout.read.return_value = b""
    mock_subprocess.return_value = mock_process

    list(tts.synthesize(input_text))

    assert mock_subprocess.call_count == 2
    
    args, _ = mock_subprocess.call_args_list[0]
    called_command = args[0]
    assert "Olá mundo." in called_command
    assert TTSConfig.COMMAND in called_command


def test_generate_audio_yields_bytes(mock_subprocess):
    tts = EspeakTTS()
    mock_process = MagicMock()
    mock_process.stdout.read.side_effect = [b"audio_chunk_1", b"audio_chunk_2", b""]
    mock_subprocess.return_value = mock_process

    audio_generator = tts._generate_audio("Teste")
    output = list(audio_generator)

    assert output == [b"audio_chunk_1", b"audio_chunk_2"]