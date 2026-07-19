from fastapi import FastAPI
import os
import google.generativeai as genai

from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

app = FastAPI()

@app.get("/")
def root():
    return {"message": "RapidAid AI Backend Running"}

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO

app = FastAPI(title="RapidAid AI Backend")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "RapidAid AI Backend Running"}

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()

        image = Image.open(BytesIO(image_bytes))

        prompt = """
You are an emergency medical AI assistant.

Analyze the uploaded injury image and return ONLY valid JSON.

Format:

{
  "injury": "",
  "severity": "Low | Medium | High",
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

Do not include markdown or explanations.
"""

        response = model.generate_content(
            [prompt, image]
        )

        return {
            "success": True,
            "analysis": response.text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
 load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")   