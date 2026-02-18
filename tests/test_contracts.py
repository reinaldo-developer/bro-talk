import pytest
from typing import Iterator
from src.interfaces.audio_input import AudioInputStrategy
from src.interfaces.transcriber import TranscriberStrategy
from src.interfaces.llm import LLMStrategy
from src.interfaces.synthesizer import SynthesizerStrategy
from src.interfaces.audio_output import AudioOutputStrategy


def test_cannot_instantiate_audio_input_without_methods():
    class IncompleteAudioInput(AudioInputStrategy):
        def start_stream(self) -> None:
            pass

    with pytest.raises(TypeError):
        IncompleteAudioInput()


def test_cannot_instantiate_transcriber_without_methods():
    class IncompleteTranscriber(TranscriberStrategy):
        pass

    with pytest.raises(TypeError):
        IncompleteTranscriber()


def test_cannot_instantiate_llm_without_methods():
    class IncompleteLLM(LLMStrategy):
        pass

    with pytest.raises(TypeError):
        IncompleteLLM()


def test_valid_llm_implementation():
    class MockLLM(LLMStrategy):
        def generate_response(self, prompt: str) -> Iterator[str]:
            yield "test"

    llm = MockLLM()
    assert isinstance(llm, LLMStrategy)


def test_cannot_instantiate_synthesizer_without_methods():
    class IncompleteSynthesizer(SynthesizerStrategy):
        pass

    with pytest.raises(TypeError):
        IncompleteSynthesizer()


def test_cannot_instantiate_audio_output_without_methods():
    class IncompleteAudioOutput(AudioOutputStrategy):
        pass

    with pytest.raises(TypeError):
        IncompleteAudioOutput()
