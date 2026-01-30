from .gemini_service import GeminiService
from gradio_client import Client
import os

class TranslationService:
    def __init__(self):
        self.gemini = GeminiService()
        self.gradio_client = None
        try:
            print("Initializing Gradio Client for Willie999/obalapalava-demo...")
            self.gradio_client = Client("Willie999/obalapalava-demo")
            print("Gradio Client initialized.")
        except Exception as e:
            print(f"Warning: Could not initialize Gradio Client. Runing in offline/mock mode. Error: {e}")

    def translate(self, text, direction, variant):
        # 1. Context Interpretation
        try:
            context = self.gemini.interpret_context(text, direction, variant)
        except Exception as e:
            print(f"Gemini Context Warning: {e}")
            context = {"normalized_text": text, "tone": "unknown", "detected_variant": variant}
            
        source_text = context.get('normalized_text', text)
        
        # 2. Translation (Force Gradio for pidgin_to_en, else Gemini)
        try:
            if direction == 'pidgin_to_en':
                translated_text = self._force_gradio_translation(source_text)
            else:
                translated_text = self._force_gemini_translation(source_text, variant)
        except Exception as e:
            print(f"CRITICAL Translation Error: {e}")
            if direction == 'pidgin_to_en':
                translated_text = "Translation not possible right now, please try again later."
            else:
                translated_text = "E be like say network dey slow, abeg try again small time."
        
        # 3. Post-processing (Only for En -> Pidgin)
        final_text = translated_text
        friendly_errors = [
            "Translation not possible right now, please try again later.",
            "E be like say network dey slow, abeg try again small time."
        ]
        
        if direction == 'en_to_pidgin' and translated_text not in friendly_errors:
            try:
                final_text = self.gemini.post_process(translated_text, variant)
            except Exception as e:
                print(f"Gemini Post-process Warning: {e}")
        
        return {
            "original": text,
            "translated": final_text,
            "context": context
        }
    
    def _force_gradio_translation(self, text):
        if not self.gradio_client:
            raise ConnectionError("Gradio Client not initialized. Cannot perform real translation.")
        
        try:
            result = self.gradio_client.predict(
                text=text,
                api_name="/translate_pidgin"
            )
            return str(result)
        except Exception as e:
            raise RuntimeError(f"Gradio Prediction Failed: {e}")
    
    def _force_gemini_translation(self, text, variant):
        if not self.gemini.api_key:
            raise ValueError("GEMINI_API_KEY missing. Cannot perform real translation.")
            
        # This is now the fallback for En -> Pidgin or any other direction Gradio doesn't handle
        prompt = f"""
        Translate the following English text to {variant} Pidgin: '{text}'.
        
        RULES:
        - Return ONLY the translated text.
        - Use English-based Pidgin (Broken English).
        - DO NOT use local languages like Twi, Ga, or Fante.
        - Ensure it sounds natural for the '{variant}' region.
        """
        result = self.gemini.generate_text(prompt)
        
        if result:
            cleaned_result = result.strip().strip("'").strip('"')
            return cleaned_result
        else:
            raise RuntimeError("Gemini failed to generate translation.")
