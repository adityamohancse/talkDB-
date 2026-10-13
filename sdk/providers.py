# sdk/providers.py

import time
from google import genai
from groq import Groq
from sdk.response import LLMResponse
from config import GOOGLE_API_KEY, GROQ_API_KEY


def call_gemini(system_prompt, user_input, model="gemini-2.0-flash"):
    """Call Google Gemini API."""
    start = time.time()
    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)
        response = client.models.generate_content(
            model=model,
            contents=user_input,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_prompt
            )
        )
        return LLMResponse(
            text=response.text,
            model_used=model,
            latency=time.time() - start
        )
    except Exception as e:
        return LLMResponse(
            text="",
            model_used=model,
            latency=time.time() - start,
            success=False,
            error=str(e)
        )


def call_groq(system_prompt, user_input, model="llama-3.3-70b-versatile"):
    """Call Groq API (Llama models)."""
    start = time.time()
    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.1
        )
        return LLMResponse(
            text=response.choices[0].message.content,
            model_used=model,
            latency=time.time() - start
        )
    except Exception as e:
        return LLMResponse(
            text="",
            model_used=model,
            latency=time.time() - start,
            success=False,
            error=str(e)
        )


# Provider registry
PROVIDERS = {
    "gemini": call_gemini,
    "groq": call_groq,
}