import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


model = genai.GenerativeModel("gemini-1.5-flash")

messages = [
    {"role": "user", "parts": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud."},
    {"role": "user", "parts": "what is coding"}
]

response = model.generate_content(messages)
print(response.text)
