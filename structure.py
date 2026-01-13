import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("Error: OPENROUTER_API_KEY not found in .env")
    exit()

# 2. Connect to OpenRouter
# OpenRouter uses the standard OpenAI client but with a different URL
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

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

print("Sending data to OpenRouter (Free Model)...")

# 5. Generate
try:
    completion = client.chat.completions.create(
        # We use the FREE version of Gemini via OpenRouter
        model="google/gemini-2.0-flash-exp:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # 6. Process Output
    response_text = completion.choices[0].message.content
    
    # Clean up potential markdown formatting (```json ... ```)
    cleaned_text = response_text.replace("```json", "").replace("```", "").strip()
    
    # Parse JSON
    data = json.loads(cleaned_text)
    
    # Save to file
    with open("final_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
    print("\nSUCCESS! Data extracted to 'final_data.json'")
    print("-" * 30)
    print("PREVIEW:")
    print(json.dumps(data.get("drawings_list", [])[:3], indent=2))

except Exception as e:
    print(f"\nERROR: {e}")