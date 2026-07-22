import logging
from google import genai
from google.genai import types
from app.config.settings import settings

logger = logging.getLogger(__name__)

class GeminiProvider:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY is not set in settings")
            self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
        return self._client

    def generate_answer(self, prompt: str) -> str:
        """
        Calls the Gemini model with the given prompt and returns the text response.
        """
        try:
            logger.info(f"Sending prompt to {settings.GEMINI_MODEL}")
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.0  # We want factual, deterministic answers from the context
                )
            )
            logger.info("Received response from Gemini")
            return response.text
        except Exception as e:
            logger.error(f"Failed during Gemini generation: {e}")
            raise Exception(f"Gemini Generation Failed: {e}")

gemini_provider = GeminiProvider()
