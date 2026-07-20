from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import json

# ==========================
# Load Environment Variables
# ==========================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable not found.")

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=api_key)

# ==========================
# FastAPI
# ==========================

app = FastAPI(
    title="RapidAid AI Backend",
    version="2.0"
)

# ==========================
# CORS
# ==========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://saivarshak.github.io",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# Home
# ==========================

@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "RapidAid AI Backend Running"
    }

# ==========================
# Debug
# ==========================

@app.get("/debug")
async def debug():
    return {
        "model": MODEL_NAME,
        "env": os.getenv("GEMINI_MODEL")
    }

# ==========================
# Analyze Image
# ==========================

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:

        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Only image files are allowed"
            )

        image_bytes = await file.read()
        
@app.get("/test")
async def test():
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents="Say hello"
    )
    return {"response": response.text}        


        prompt = """
You are RapidAid AI, an emergency first-aid assistant.

Analyze the uploaded injury image carefully.

Return ONLY valid JSON.

JSON format:

{
  "injury": "",
  "severity": "Low/Medium/High",
  "confidence": "",
  "description": "",
  "first_aid": [
    "",
    "",
    ""
  ],
  "recommended_specialist": "",
  "emergency": true
}

Rules:
- Do NOT give a final medical diagnosis.
- Only provide first-aid guidance.
- Recommend medical attention whenever appropriate.
"""

        response = client.models.generate_content(
    model=MODEL_NAME,
    contents=[
        prompt,
        types.Part.from_bytes(
            data=image_bytes,
            mime_type=file.content_type,
        ),
    ],
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    ),
)

        try:
            analysis = json.loads(text)
        except Exception:
            analysis = {
                "raw_response": text
            }

        return {
            "success": True,
            "analysis": analysis
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Gemini Error:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ==========================
# Run
# ==========================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )