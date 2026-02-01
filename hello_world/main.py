from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an expert in the field of AI. Only answer questions related to AI. Otherwise, say 'I'm sorry, I can only answer questions related to AI.'"},
        {"role": "user", "content": "Hey there! I am Tarique Anjum. Nice to meet you! How is the weather in Tokyo?"}
    ]
)

print(response.choices[0].message.content)
