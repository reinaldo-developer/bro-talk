from gtts import gTTS
from playsound import playsound
import os

temp_audio_file = "temporary_audio_conversion_file.mp3"

def speak(text):
    if not text:
        print("Nenhum texto para falar")
        return
    print("🎤 Gerando audio")

    try:
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(temp_audio_file)

        playsound(temp_audio_file)
    except Exception as e:
        print(f"Ocorreu um erro ao tentar usar o gTTS: {e}")
    finally:
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)

if __name__ == "__main__":
    text = "Hello, this is a test of speak conversion."
    speak(text=text)