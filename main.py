
import os
import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from openai import OpenAI

app = FastAPI(title="InstaWing AI")


class SuggestRequest(BaseModel):
    profile_notes: str = Field(default="", max_length=1500)
    latest_message: str = Field(default="", max_length=2000)
    tone: str = Field(default="flirty but respectful", max_length=80)


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/manifest.json")
def manifest():
    return FileResponse("manifest.json")


@app.get("/sw.js")
def worker():
    return FileResponse("sw.js")


@app.get("/health")
def health():
    return {"ok": True, "service": "InstaWing AI"}


@app.post("/api/suggest")
def suggest(req: SuggestRequest):
    key = os.getenv("OPENAI_API_KEY")

    if not key:
        return {
            "mode": "demo",
            "suggestions": [
                "Your profile has a good vibe. What are you into lately?",
                "Spontaneous plans or perfectly planned ones? 😄",
                "I think we might share a few interests. What's been keeping you busy?"
            ]
        }

    try:
        client = OpenAI(api_key=key)

        prompt = f"""
Generate exactly 3 short Instagram conversation suggestions.

Tone: {req.tone}
Be natural, confident, playful and respectful.
No pressure, manipulation or sexual comments.
Do not assume gender or relationship status.
Use only the supplied context.

Profile notes: {req.profile_notes or '(none)'}
Latest message: {req.latest_message or '(first opener)'}

Return JSON with a key named suggestions containing 3 strings.
"""

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": "You are a respectful conversation assistant."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.8
        )

        data = json.loads(
            response.choices[0].message.content or "{}"
        )

        suggestions = [
            str(x).strip()
            for x in data.get("suggestions", [])
            if str(x).strip()
        ][:3]

        if len(suggestions) != 3:
            raise ValueError("Expected three suggestions")

        return {"mode": "live", "suggestions": suggestions}

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AI request failed: {type(exc).__name__}"
        )
        
