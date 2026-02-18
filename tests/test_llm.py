import pytest
from unittest.mock import MagicMock
from src.infrastructure.llm.ollama_service import OllamaLLM
from src.domain.config import LLMConfig


@pytest.fixture
def mock_ollama_client():
    return MagicMock()


def test_llm_initialization(mock_ollama_client):
    llm = OllamaLLM(client=mock_ollama_client)
    assert llm._client == mock_ollama_client
    assert llm._model == LLMConfig.MODEL


def test_generate_response_streams_content(mock_ollama_client):
    llm = OllamaLLM(client=mock_ollama_client)

    mock_stream_response = [
        {"message": {"content": "Olá"}},
        {"message": {"content": " "}},
        {"message": {"content": "mundo"}},
        {"done": True},
    ]
    mock_ollama_client.chat.return_value = iter(mock_stream_response)

    response_generator = llm.generate_response("Teste")

    tokens = list(response_generator)
    assert tokens == ["Olá", " ", "mundo"]

    mock_ollama_client.chat.assert_called_once_with(
        model=LLMConfig.MODEL,
        messages=[{"role": "user", "content": "Teste"}],
        stream=True,
    )


def test_generate_response_handles_empty_chunks(mock_ollama_client):
    llm = OllamaLLM(client=mock_ollama_client)

    mock_stream_response = [
        {"message": {"content": "Test"}},
        {},
        {"message": {}},
        {"message": {"content": "ing"}},
    ]
    mock_ollama_client.chat.return_value = iter(mock_stream_response)

    tokens = list(llm.generate_response("Teste"))
    assert tokens == ["Test", "ing"]