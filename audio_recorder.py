import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import queue
import time

class AudioRecorder:
    def __init__(self, silence_threshold=10000, silence_duration=1.0, debug=False):
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.sample_rate = 44100
        self.blocksize = 1024
        self.q = queue.Queue()
        self.debug = debug

    def _callback(self, indata, frames, time_info, status):
        if status:
            print(status)
        self.q.put(indata.copy())
    
    def record_audio(self, file_name="temp_user_speech.wav"):
        print("🎤 Ouvindo...")

        audio_data = []
        start_time = last_sound_time = time.time()
        has_spoken = False

        with sd.InputStream(samplerate=self.sample_rate, channels=1,
                            callback=self._callback, dtype='int16',
                            blocksize=self.blocksize):
            while True:
                chunk = self.q.get(timeout=0.5)
                audio_data.append(chunk)
                volume = np.max(np.abs(chunk))

                if self.debug:
                    print(f"Volume: {volume} | Threshold: {self.silence_threshold}")
                current_time = time.time()

                if volume > self.silence_threshold:
                    last_sound_time = current_time
                    if not has_spoken:
                        print("🗣️ Voz detectada!")
                        has_spoken = True
                
                # Lógica de parada por silêncio
                if has_spoken and ((current_time - last_sound_time) > self.silence_duration):
                    print("✅ Silêncio detectado. Parando.")
                    break
                
                # Timeout absoluto (segurança para não ficar preso para sempre)
                if not has_spoken and ((current_time - start_time) > 10):
                    print("⏰ Timeout: Ninguém falou.")
                    break
                
                # Timeout se a pessoa falar por muito tempo (ex: 60 segundos)
                if ((current_time - start_time) > 60):
                     print("🛑 Limite máximo de tempo atingido.")
                     break
        recording = np.concatenate(audio_data, axis=0)
        write(file_name, self.sample_rate, recording)
        return file_name


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
    recorder = AudioRecorder()
    file = recorder.record_audio()

