# app/ai_services.py

import os
import openai
from dotenv import load_dotenv

# Load environment variables (including OPENAI_API_KEY)
load_dotenv()

# Get the OpenAI API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Optional: read additional ChatGPT settings from .env
CHATGPT_MODEL = os.getenv("CHATGPT_MODEL", "gpt-3.5-turbo")
CHATGPT_MAX_TOKENS = int(os.getenv("CHATGPT_MAX_TOKENS", 200))
CHATGPT_TEMPERATURE = float(os.getenv("CHATGPT_TEMPERATURE", 0.5))

def chatgpt_summarize(text: str) -> str:
    """
    Summarizes the given text using the OpenAI ChatCompletion API.
    """
    if not openai.api_key:
        return "OpenAI API key not configured."

    try:
        response = openai.ChatCompletion.create(
            model=CHATGPT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes user notes."
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text:\n\n{text}"
                }
            ],
            max_tokens=CHATGPT_MAX_TOKENS,
            temperature=CHATGPT_TEMPERATURE
        )
        summary = response.choices[0].message["content"].strip()
        return summary
    except Exception as e:
        print("ChatGPT Summarization Error:", e)
        return "Summary not available."