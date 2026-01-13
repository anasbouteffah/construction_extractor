from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("Fetching available models...")
for m in client.models.list():
    if "generateContent" in m.supported_generation_methods:
        print(f"- {m.name}")