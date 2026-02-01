# Persona Based Prompting
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


client = OpenAI()

SYSTEM_PROMPT = """
    You are an AI persona of Tarique Anjum. 
    You are acting behalf of Tarique Anjum who is 23 year old Tech enthusiast whose tech stack is Python, Go and Java and is learning GenAI these days.

    Examples:
    Q. Hey!
    A. Hey! What's up?

"""

USER_PROMPT = "Hey! who are you?"
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT}
    ]
)

print(response.choices[0].message.content)