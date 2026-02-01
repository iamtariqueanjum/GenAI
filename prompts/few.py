from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = f"""You are Ahmed. Only answer questions related to coding. 
Otherwise, say 'I'm sorry, I can only answer questions related to coding.'

Rule:
- Strictly follow the output in JSON format.
Output Format:
{{"code": "string" or null,
  "isCodingQuestion": boolean}}

Here are some examples:
Example 1:
Question: How is the weather in Tokyo?
Answer: {{"code": null, "isCodingQuestion": false}}

Example 2:
Question: Write a python code to add two numbers.
Answer: {{"isCodingQuestion": true, "code": " def add(a, b):
            return a + b"}}
"""

USER_PROMPT = "Hey there! I am Tarique Anjum. Nice to meet you! Write a python code to add two numbers.?"

# Few Shot Prompting - The model is given a question or task with prior examples.
response = client.chat.completions.create(model="gemini-3-flash-preview", messages=[
    {"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": USER_PROMPT}
    ])
print(response.choices[0].message.content)
