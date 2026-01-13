import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
import nest_asyncio

# This fixes some issues with event loops in certain environments
nest_asyncio.apply()

# 1. Load your API keys from the .env file
load_dotenv()

# Verify keys are loaded (prints "Yes" or "No", doesn't show the key)
print(f"Llama Cloud Key present: {'Yes' if os.getenv('LLAMA_CLOUD_API_KEY') else 'No'}")
print(f"Google API Key present: {'Yes' if os.getenv('GOOGLE_API_KEY') else 'No'}")

# 2. Setup the LlamaParse Tool
# result_type="markdown". LLMs understand formatting better in markdown.
parser = LlamaParse(
    result_type="markdown",
    verbose=True,
    language="en"
)

# 3. Process the PDF
pdf_name = "PLN23_116_R1_Plans.pdf" 
print(f"\nProcessing {pdf_name}... this might take a minute...")

try:
    documents = parser.load_data(pdf_name)
    
    # 4. Save the result so we can look at it
    output_file = "extracted_text.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(documents[0].text)
        
    print(f"\nSUCCESS! Content saved to {output_file}")
    print("-" * 20)
    print("PREVIEW OF EXTRACTED TEXT:")
    print(documents[0].text[:500]) # Print the first 500 characters
    
except Exception as e:
    print(f"\nERROR: {e}")