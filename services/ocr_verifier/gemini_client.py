import os, json, asyncio
from typing import Dict, Any
from fastapi import HTTPException
from dotenv import load_dotenv
from google import genai
from google.genai import types as gtypes

from services.ocr_verifier.constants import REGEX_PATTERNS, VERIFICATION_SCHEMA

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment")

client = genai.Client(api_key=API_KEY)

async def verify_with_gemini(raw_text: str, doc_type: str) -> Dict[str, Any]:
    prompt = f"""
    You are an AI Document Validator for Indian documents.
    Document type: {doc_type.upper()}

    Apply regex:
    PAN: {REGEX_PATTERNS['PAN_CARD']}
    AADHAAR: {REGEX_PATTERNS['AADHAAR_NO']}
    DOB: {REGEX_PATTERNS['DATE_FORMAT']}

    Return STRICT JSON schema.
    ---
    {raw_text[:4000]}
    ---
    """

    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.5-flash",
            contents=[prompt],
            config=gtypes.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=VERIFICATION_SCHEMA
            ),
        )
        return json.loads(response.text)
    except Exception as e:
        raise HTTPException(500, f"Gemini verification failed: {e}")
