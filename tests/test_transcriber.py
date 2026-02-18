import pytest
from unittest.mock import MagicMock, PropertyMock
from src.infrastructure.stt.whisper_service import WhisperTranscriber


def test_transcriber_uses_injected_model():
    mock_model = MagicMock()
    transcriber = WhisperTranscriber(model=mock_model)

    segment = MagicMock()
    type(segment).text = PropertyMock(return_value="Teste")
    mock_model.transcribe.return_value = ([segment], None)

    fake_audio = b"\x00"
    transcriber.transcribe(fake_audio)

    mock_model.transcribe.assert_called_once()


def test_transcribe_returns_formatted_text():
    mock_model = MagicMock()
    transcriber = WhisperTranscriber(model=mock_model)

    segment1 = MagicMock()
    type(segment1).text = PropertyMock(return_value="Olá")
    segment2 = MagicMock()
    type(segment2).text = PropertyMock(return_value="mundo")

    mock_model.transcribe.return_value = ([segment1, segment2], None)

    result = transcriber.transcribe(b"\x00")

    assert result == "Olá mundo"