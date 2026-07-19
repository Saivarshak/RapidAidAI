from fastapi import FastAPI

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
    # Validate image type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload a valid image.")

    try:
        # Read uploaded file
        image_bytes = await file.read()

        # Open image
        image = Image.open(BytesIO(image_bytes))

        # Get image details
        width, height = image.size

        # Temporary response (replace later with Gemini AI analysis)
        return {
            "success": True,
            "filename": file.filename,
            "content_type": file.content_type,
            "width": width,
            "height": height,
            "message": "Image uploaded successfully. Ready for AI analysis."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))