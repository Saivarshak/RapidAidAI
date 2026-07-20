from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types
import os
import json


# Load environment variables
load_dotenv()


# ==========================
# Gemini Configuration
# ==========================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable not found."
    )

client = genai.Client(api_key=api_key)

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


# ==========================
# FastAPI Application
# ==========================

app = FastAPI(
    title="RapidAid AI Backend",
    version="1.0"
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
# Home Route
# ==========================

@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "RapidAid AI Backend Running"
    }


# ==========================
# AI Image Analysis API
# ==========================

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):

    try:

        # Check file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Only image files are allowed"
            )


        # Read image
        image_bytes = await file.read()

        image = Image.open(
            BytesIO(image_bytes)
        )



        prompt = """
You are RapidAid AI, an emergency first-aid assistant.

Analyze the uploaded injury image carefully.

Return ONLY valid JSON.

Do not use markdown.
Do not add explanations outside JSON.

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

Important:
- Do not give a final medical diagnosis.
- Provide emergency guidance only.
- Recommend professional medical help when needed.
"""


     response = client.models.generate_content(
    model=MODEL_NAME,
    contents=[
        prompt,
        image
    ],
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)

text = response.text.strip()


        # Remove markdown if Gemini returns it
        if "```json" in text:
            text = (
                text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        elif "```" in text:
            text = (
                text
                .replace("```", "")
                .strip()
            )


        # Convert JSON response
        try:

            analysis_result = json.loads(text)

        except Exception:

            analysis_result = {
                "raw_response": text
            }


        return {

            "success": True,

            "analysis": analysis_result

        }


    except HTTPException:

        raise


    except Exception as e:

        print(
            "Gemini Error:",
            str(e)
        )

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )



# ==========================
# Run Server
# ==========================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "main:app",

        host="0.0.0.0",

        port=8000,

        reload=True

    )
@app.get("/debug")
async def debug():
    return {
        "model": MODEL_NAME,
        "env": os.getenv("GEMINI_MODEL")
    }
    