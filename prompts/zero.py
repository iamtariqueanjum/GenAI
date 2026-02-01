from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = "You are Ahmed. Only answer questions related to coding. Otherwise, say 'I'm sorry, I can only answer questions related to coding.'"


# Zero Shot Prompting - The model is given a direct question or task without prior examples.
response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey there! I am Tarique Anjum. Nice to meet you! What is loops in python?"}
    ]
)

print(response.choices[0].message.content)
