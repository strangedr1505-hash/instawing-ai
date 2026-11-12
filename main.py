import os, json
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from openai import OpenAI

app=FastAPI(title="InstaWing AI")
app.mount("/static",StaticFiles(directory="static"),name="static")

class Request(BaseModel):
    profile_notes:str=Field(default="",max_length=1500)
    latest_message:str=Field(default="",max_length=2000)
    tone:str=Field(default="flirty but respectful",max_length=80)

@app.get("/")
def home(): return FileResponse("static/index.html")
@app.get("/manifest.json")
def manifest(): return FileResponse("static/manifest.json",media_type="application/manifest+json")
@app.get("/sw.js")
def worker(): return FileResponse("static/sw.js",media_type="application/javascript")
@app.get("/health")
def health(): return {"ok":True}

@app.post("/api/suggest")
def suggest(req:Request):
    key=os.getenv("OPENAI_API_KEY")
    if not key:
        if req.latest_message.strip():
            suggestions=["That’s an interesting take 😄 What got you into that?","Okay, I need the story behind that one 👀","I like your perspective. What happened next?"]
        else:
            suggestions=["Your profile has a good vibe — what’s something you’re really into lately?","Quick question: spontaneous plans or perfectly planned ones? 😄","I noticed we might share a few interests. What have you been enjoying lately?"]
        return {"suggestions":suggestions,"mode":"demo"}
    try:
        client=OpenAI(api_key=key)
        prompt=f"""Create exactly 3 short Instagram conversation suggestions. Tone: {req.tone}.
Be warm, confident, lightly playful and respectful. No sexual comments, pressure,
manipulation, negging, fake familiarity, or unsupported assumptions. Do not assume
gender or relationship status. If no reply has arrived, do not suggest repeated follow-ups.
Use only the context supplied. Return JSON: {{\"suggestions\":[\"...\",\"...\",\"...\"]}}.
Profile notes: {req.profile_notes or '(none)'}
Latest message: {req.latest_message or '(first opener)'}"""
        res=client.chat.completions.create(model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),
            messages=[{"role":"system","content":"You are a respectful conversation-writing assistant."},{"role":"user","content":prompt}],
            response_format={"type":"json_object"},temperature=0.8)
        items=json.loads(res.choices[0].message.content or "{}").get("suggestions",[])
        items=[str(x).strip() for x in items if str(x).strip()][:3]
        if len(items)!=3: raise ValueError("Expected 3 suggestions")
        return {"suggestions":items,"mode":"live"}
    except Exception as e:
        raise HTTPException(status_code=502,detail=f"AI request failed: {type(e).__name__}")

