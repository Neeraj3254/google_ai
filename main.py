import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel('models/gemini-2.5-pro')

prompt = input("enter your prompt: ")
response = model.generate_content(prompt)
print(response.text)

# Save to file
with open("responses.txt", "a", encoding="utf-8") as f:
    f.write(f"Prompt: {prompt}\n")
    f.write(f"Response: {response.text}\n")
    f.write("-" * 60 + "\n")
