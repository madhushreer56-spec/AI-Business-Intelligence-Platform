import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found."
    )

client = genai.Client(
    api_key=API_KEY
)


def generate_content(prompt, retries=3):

    last_error = None

    for attempt in range(retries):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            if not response.text:
                raise Exception(
                    "Gemini returned an empty response."
                )

            return response.text.strip()

        except Exception as e:

            last_error = e
            error = str(e)

            if "503" in error or "UNAVAILABLE" in error:

                time.sleep(2 * (attempt + 1))
                continue

            if "429" in error:

                time.sleep(5 * (attempt + 1))
                continue

            raise Exception(
                f"Gemini API Error:\n\n{error}"
            )

    raise Exception(
        f"Gemini unavailable after {retries} attempts:\n\n"
        f"{last_error}"
    )