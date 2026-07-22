import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

client = genai.Client(
    api_key=API_KEY
)


# ==========================================================
# Safe Gemini Call
# ==========================================================

def generate_content(prompt, retries=3):

    last_error = None

    for attempt in range(retries):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text.strip()

        except Exception as e:

            last_error = e

            error = str(e)

            # Retry if Gemini is temporarily unavailable
            if "503" in error or "UNAVAILABLE" in error:

                time.sleep(2 * (attempt + 1))
                continue

            # Retry if rate limited
            if "429" in error:

                time.sleep(5)
                continue

            raise e

    raise last_error