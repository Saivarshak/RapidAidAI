from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import google.generativeai as genai
import os
import json

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable not found.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI(title="RapidAid AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://saivarshak.github.io",
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "RapidAid AI Backend Running"
    }


@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:

        image_bytes = await file.read()

        image = Image.open(BytesIO(image_bytes))

        prompt = """
You are an emergency medical AI assistant.

Analyze the injury image.

Return ONLY valid JSON.

{
  "injury":"",
  "severity":"Low",
  "confidence":"95%",
  "description":"",
  "first_aid":[
      "",
      "",
      ""
  ],
  "recommended_specialist":"",
  "emergency":true
}
"""

        response = model.generate_content([prompt, image])

        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        try:
            result = json.loads(text)
        except:
            result = {
                "raw_response": text
            }

        return {
            "success": True,
            "analysis": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

print("API KEY:", api_key)        