import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    print("❌ GEMINI_API_KEY not found")
    exit()

genai.configure(api_key=api_key)

print("=" * 60)
print("Available Gemini Models")
print("=" * 60)

try:
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            print(model.name)
except Exception as e:
    print("Error:", e)


import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content("Say Hello")

print(response.text)