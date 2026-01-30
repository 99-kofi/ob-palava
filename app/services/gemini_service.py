from google import genai
import os
import json
import re

class GeminiService:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            print("Warning: Gemini API Key not found.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)
        
        # Models to try in order of preference
        # User requested gemini-3-flash-preview, but gemini-flash-latest has higher limits.
        # Gemma models are added as emergency fallbacks since they often have separate quotas.
        self.models = [
            "gemini-3-flash-preview", 
            "gemini-2.0-flash", 
            "gemini-flash-latest", 
            "gemini-pro-latest",
            "gemma-3-27b-it",
            "gemma-3-12b-it"
        ]

    def _call_gemini(self, prompt):
        if not self.client:
            return None

        for model_id in self.models:
            try:
                print(f"Calling Gemini with model: {model_id}...")
                response = self.client.models.generate_content(
                    model=model_id,
                    contents=prompt,
                )
                
                if response and response.text:
                    return response.text
                else:
                    print(f"Gemini Warning: No text found in response from {model_id}.")
                    continue # Try next model
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    print(f"Quota exceeded for {model_id}. Trying fallback...")
                    continue # Try next model
                
                print(f"Gemini SDK Call failed for {model_id}: {e}")
                return None
        
        print("All Gemini fallback models exhausted.")
        return None

    def generate_text(self, prompt):
        return self._call_gemini(prompt)

    def interpret_context(self, text, direction, variant):
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY missing for real testing.")
        
        prompt = f"""
        Analyze the following text for translation context: "{text}"
        Direction: {direction}
        Variant: {variant}
        
        CRITICAL: Return ONLY raw JSON. Do not include any explanation or conversational text.
        
        Required JSON structure:
        {{
            "normalized_text": "string",
            "tone": "string",
            "detected_variant": "string"
        }}
        """
        
        result_text = self._call_gemini(prompt)
        
        if result_text:
            try:
                # More aggressive JSON extraction
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                
                cleaned_text = re.sub(r'```json\s*|\s*```', '', result_text).strip()
                return json.loads(cleaned_text)
            except Exception as e:
                print(f"JSON Parse Error: {e}. Raw text: {result_text}")
                # Fallback context if JSON fails
                return {"normalized_text": text, "tone": "unknown", "detected_variant": variant}
        
        raise RuntimeError("Gemini/Gemma failed to return context analysis.")

    def post_process(self, translated_text, target_variant):
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY missing for real testing.")
            
        prompt = f"""
        Polish this translation into authentic {target_variant} Pidgin: "{translated_text}"
        
        STRICT RULES:
        1. Return ONLY the polished translation.
        2. NO explanations or conversational filler.
        3. NO local Ghanaian languages like Twi, Fante, or Ewe. This MUST be English-based Pidgin (Broken English).
        4. Use authentic urban slang common in {target_variant}.
        5. DO NOT provide alternate versions.
        """
        
        result_text = self._call_gemini(prompt)
        if not result_text:
            raise RuntimeError("Gemini/Gemma failed to post-process translation.")
        
        # Clean up any potential conversational filler from models like Gemma
        lines = result_text.strip().split('\n')
        # Return the first non-empty line that doesn't look like an intro
        for line in lines:
            line = line.strip()
            if line and not line.lower().startswith(("here is", "this is", "refined", "sure")):
                return line
                
        return lines[0].strip()
