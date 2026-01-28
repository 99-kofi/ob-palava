import requests
import os
import uuid

class TTSService:
    def __init__(self, static_folder):
        self.audio_folder = os.path.join(static_folder, 'audio')
        if not os.path.exists(self.audio_folder):
            os.makedirs(self.audio_folder)
        self.api_url = "https://yarngpt.ai/api/v1/tts"
        self.api_key = os.environ.get("YARNGPT_API_KEY")

    def generate_audio(self, text, variant='ghana', direction='en_to_pidgin'):
        # If target is English (pidgin_to_en), use Google TTS
        if direction == 'pidgin_to_en':
            return self._generate_google_tts(text)
        
        # Otherwise use YarnGPT for Pidgin
        return self._generate_yarngpt_tts(text)

    def _generate_google_tts(self, text):
        from gtts import gTTS
        try:
            filename = f"en_{uuid.uuid4()}.mp3"
            filepath = os.path.join(self.audio_folder, filename)
            
            tts = gTTS(text=text, lang='en')
            tts.save(filepath)
            
            return f"/static/audio/{filename}"
        except Exception as e:
            print(f"Google TTS Error: {e}")
            return None

    def _generate_yarngpt_tts(self, text):
        if not self.api_key:
            print("Error: YARNGPT_API_KEY not found.")
            return None

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "text": text,
                "voice": "Tayo",
            }

            response = requests.post(self.api_url, headers=headers, json=payload, stream=True, timeout=30)
            
            if response.status_code == 200:
                filename = f"pidgin_{uuid.uuid4()}.mp3"
                filepath = os.path.join(self.audio_folder, filename)
                
                with open(filepath, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return f"/static/audio/{filename}"
            else:
                print(f"YarnGPT Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"YarnGPT TTS Error: {e}")
            return None
