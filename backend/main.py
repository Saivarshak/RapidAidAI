from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from google import genai
import os

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app = FastAPI(title="RapidAid AI Backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://saivarshak.github.io"
    ],
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

Analyze the uploaded injury image.

Return ONLY valid JSON.

{
  "injury":"",
  "severity":"Low | Medium | High",
  "confidence":"",
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

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image]
        )

        return {
            "success": True,
            "analysis": response.text
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )