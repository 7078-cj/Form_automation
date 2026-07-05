import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("AI_KEY")
)


def generate(prompt):
    """
    Sends prompt to Gemini and returns strict JSON.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        if not response.text:
            return {
                "success": False,
                "error": "Gemini returned an empty response."
            }

        parsed = json.loads(response.text)

        return {
            "success": True,
            "result": parsed
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "Gemini did not return valid JSON.",
            "raw_text": response.text if "response" in locals() else None
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }