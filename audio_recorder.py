import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

SAMPLE_RATE = 44100 #standard sample rate
TEMPORARY_RECORD_FILE_NAME = "temp_user_speech.wav"

def record_audio(duration_seconds=10):
    print(f"🎤 gravando {duration_seconds}s de voz do usuário")

    recording = sd.rec(
        int(duration_seconds*SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.int16
    )
    sd.wait()

    write(TEMPORARY_RECORD_FILE_NAME, SAMPLE_RATE, recording)
    print(f"✅ Áudio salvo como {TEMPORARY_RECORD_FILE_NAME}")
    
    return TEMPORARY_RECORD_FILE_NAME

if __name__ == "__main__":
    print("Vamos testar o gravador de voz")
    record_audio()