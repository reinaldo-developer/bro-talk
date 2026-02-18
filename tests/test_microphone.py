import pytest
from unittest.mock import MagicMock, patch
from src.infrastructure.io.microphone import MicrophoneInput
from src.interfaces.vad import VADStrategy
from src.domain.config import AudioConfig


@pytest.fixture
def mock_pyaudio():
    with patch("src.infrastructure.io.microphone.pyaudio.PyAudio") as mock:
        yield mock


@pytest.fixture
def mock_vad_strategy():
    return MagicMock(spec=VADStrategy)


def test_microphone_initialization(mock_pyaudio, mock_vad_strategy):
    mic = MicrophoneInput(vad_strategy=mock_vad_strategy)
    assert mic._stream is None
    mock_pyaudio.assert_called()


def test_start_stream_config(mock_pyaudio, mock_vad_strategy):
    mic = MicrophoneInput(vad_strategy=mock_vad_strategy)
    mic.start_stream()

    mock_pyaudio.return_value.open.assert_called_once_with(
        format=AudioConfig.FORMAT,
        channels=AudioConfig.CHANNELS,
        rate=AudioConfig.SAMPLE_RATE,
        input=True,
        frames_per_buffer=AudioConfig.CHUNK_SIZE,
        input_device_index=None,
    )


def test_stop_stream(mock_pyaudio, mock_vad_strategy):
    mic = MicrophoneInput(vad_strategy=mock_vad_strategy)
    mock_stream = MagicMock()
    mock_pyaudio.return_value.open.return_value = mock_stream

    mic.start_stream()
    mic.stop_stream()

    mock_stream.stop_stream.assert_called_once()
    mock_stream.close.assert_called_once()
    mock_pyaudio.return_value.terminate.assert_called_once()


def test_listen_yields_audio_after_speech_detected(mock_pyaudio, mock_vad_strategy):
    mic = MicrophoneInput(vad_strategy=mock_vad_strategy)
    mock_stream = MagicMock()
    mock_stream.is_active.return_value = True

    fake_chunk = b"\x00" * 640

    mock_stream.read.return_value = fake_chunk
    mock_pyaudio.return_value.open.return_value = mock_stream

    vad_results = [False] * 5 + [True] * 5 + [False] * 60
    mock_vad_strategy.is_speech.side_effect = vad_results

    generator = mic.listen()

    try:
        result = next(generator)
        assert len(result) > 0
        assert isinstance(result, bytes)
    except StopIteration:
        pytest.fail("Generator stopped without yielding")

    mic._is_listening = False