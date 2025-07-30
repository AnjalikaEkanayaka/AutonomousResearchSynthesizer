import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read Gemini API key
key = os.getenv("GEMINI_API_KEY")

if key:
    print(" Gemini API Key Loaded Successfully!")
else:
    print(" Failed to load Gemini API Key")
