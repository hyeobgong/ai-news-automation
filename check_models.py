import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API Key not found")
else:
    client = genai.Client(api_key=api_key)
    try:
        print("Available models:")
        for model in client.models.list(config={"page_size": 100}):
            print(f"- {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")