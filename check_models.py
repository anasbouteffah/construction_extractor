from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("Fetching available models...")

# The new SDK returns a list of objects that have a '.name' attribute
# We simply print that name.
try:
    for m in client.models.list():
        print(f" - {m.name}")
except Exception as e:
    print(f"Error: {e}")