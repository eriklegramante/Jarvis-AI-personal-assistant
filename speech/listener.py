import io
import speech_recognition as sr
from faster_whisper import WhisperModel
import torch

class JarvisListener:
    def __init__(self, model_size="base"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = WhisperModel(model_size, device=self.device, compute_type="int8")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(sample_rate=16000)

    def wait_for_wake_word(self, wake_words=["jarvis", "ok jarvis"]):
        """Fica em standby monitorando apenas a palavra de ativação."""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=3)
                audio_data = io.BytesIO(audio.get_wav_data())
                
                segments, _ = self.model.transcribe(audio_data, language="pt", beam_size=1)
                text = "".join([s.text for s in segments]).lower().strip()
                
                return any(word in text for word in wake_words)
            except:
                return False        
    

    def listen(self):
        """Sua função atual, otimizada para comandos complexos."""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1.5) 
            self.recognizer.energy_threshold = 400
            self.recognizer.pause_threshold = 0.8
            
            print("\n[OUVINDO COMANDO...]")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                return ""

        try:
            print("[PROCESSANDO...]")
            audio_data = io.BytesIO(audio.get_wav_data())
            
            segments, info = self.model.transcribe(
                audio_data, 
                beam_size=5, 
                language="pt",
                initial_prompt="Jarvis, sistema, rede, comandos, computador, tecnologia.",
                condition_on_previous_text=False, 
                repetition_penalty=1.2,           
                no_speech_threshold=0.6          
            )
            
            full_text = "".join([segment.text for segment in segments])
            return full_text.strip()
        
        except Exception as e:
            print("Erro na transcrição:", e)
            return ""
    
        