import os
import json
import time
import urllib.request
import urllib.error
from typing import Dict

from google import genai

_gemini_client = None


def _get_gemini_client():
    global _gemini_client
    if _gemini_client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Check your .env file.")
        _gemini_client = genai.Client(api_key=api_key)
    return _gemini_client


def _call_nvidia(prompt: str, max_retries: int = 3) -> Dict:
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY not found. Check your .env file.")
    model = os.environ.get("NVIDIA_MODEL", "nvidia/nemotron-super-120b-instruct")

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "ענה בעברית בלבד. אל תשתמש במילים באנגלית או בשפות אחרות."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 8000,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://integrate.api.nvidia.com/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            msg = body["choices"][0]["message"]
            text = (msg.get("content") or msg.get("reasoning_content") or "").strip()
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            return json.loads(text.strip())
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error ({attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                raise
        except urllib.error.HTTPError as e:
            status = e.code
            if status == 429:
                wait = 30 * (attempt + 1)
                print(f"⏳ Rate limit. Waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"⚠️ NVIDIA API error {status} ({attempt + 1}/{max_retries}): {e.reason}")
                if attempt == max_retries - 1:
                    raise
        except TimeoutError as e:
            wait = 15 * (attempt + 1)
            print(f"⏳ Timeout ({attempt + 1}/{max_retries}). Waiting {wait}s before retry...")
            time.sleep(wait)
            if attempt == max_retries - 1:
                raise
        except Exception as e:
            if "timed out" in str(e).lower() or "timeout" in str(e).lower():
                wait = 15 * (attempt + 1)
                print(f"⏳ Timeout ({attempt + 1}/{max_retries}). Waiting {wait}s before retry...")
                time.sleep(wait)
                if attempt == max_retries - 1:
                    raise
            else:
                print(f"⚠️ Error ({attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    raise
    raise Exception("Failed after retries")


def _call_gemini(prompt: str, max_retries: int = 3) -> Dict:
    client = _get_gemini_client()
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="models/gemini-flash-latest",
                contents=prompt,
            )
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            return json.loads(text.strip())
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error ({attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                raise
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                wait = 20 * (attempt + 1)
                print(f"⏳ Rate limit. Waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"⚠️ API error ({attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    raise
    raise Exception("Failed after retries")


def call_gemini(prompt: str, max_retries: int = 3) -> Dict:
    provider = os.environ.get("LLM_PROVIDER", "gemini").lower()
    if provider == "nvidia":
        return _call_nvidia(prompt, max_retries)
    return _call_gemini(prompt, max_retries)
