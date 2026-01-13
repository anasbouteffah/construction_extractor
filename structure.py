import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Prepare the Client (New Syntax)
# The new SDK handles the connection differently
client = genai.Client(api_key=api_key)

# 3. Read the Markdown file
try:
    with open("extracted_text.md", "r", encoding="utf-8") as f:
        markdown_content = f.read()
except FileNotFoundError:
    print("Error: 'extracted_text.md' not found. Did you run step 1?")
    exit()

# 4. The Prompt
prompt = f"""
You are an expert Data Engineer for the construction industry.
Your goal is to extract structured data from the provided Construction Plan text.

RULES:
1. Extract the "Project Information" (Name, Address, Date) if available.
2. Extract the "Index of Drawings" as a list of objects.
3. Output strictly valid JSON. Do not write markdown blocks (```json).

INPUT TEXT:
{markdown_content}

REQUIRED JSON STRUCTURE:
{{
  "project_info": {{
    "name": "string",
    "address": "string",
    "date": "string"
  }},
  "drawings_list": [
    {{
      "sheet_number": "string",
      "description": "string",
      "revision": "string"
    }}
  ],
  "summary": "A 1-sentence summary of what this document is."
}}
"""

print("Sending data to Gemini (New SDK)...")

# 5. Generate (New Syntax)
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite-preview-02-05",  # Using the newer, faster model
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json" # Forces JSON output natively
        )
    )

    # 6. Save Output
    # The new SDK returns data in response.text
    cleaned_text = response.text
    
    # Parse and Save
    data = json.loads(cleaned_text)
    
    with open("final_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
    print("\nSUCCESS! Data extracted to 'final_data.json'")
    print("-" * 30)
    print("PREVIEW:")
    # Print first 2 items to verify
    print(json.dumps(data.get("drawings_list", [])[:2], indent=2))

except Exception as e:
    print(f"\nERROR: {e}")