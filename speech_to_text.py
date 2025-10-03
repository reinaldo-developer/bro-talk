import whisper
import os

try:
    speech_to_text_model = whisper.load_model("base")
except Exception as e:
    print(f"Erro ao carregar o modelo Whisper: {e}")
    speech_to_text_model = None

def transcribe(audio_filename) -> str:
    if not speech_to_text_model:
        return "Model not loaded"
    if not os.path.exists(audio_filename):
        return "audio provisory file not found"
    print("Transcrevendo audio")

    try:
        transcription_object = speech_to_text_model.transcribe(audio_filename, fp16=False, language="en")
        text = transcription_object.get("text", "")
        return text
    except Exception as e:
        print(f"Ocorreu um erro na transcrição: {e}")
        return ""
    
if __name__ == '__main__':
    from audio_recorder import record_audio
    audio_to_conversion = record_audio(duration_seconds=4)
    print(f"file_path={audio_to_conversion}")
    transcription = transcribe(audio_to_conversion)
    print(transcription)