from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()



response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{
        "role": "user", 
        "content": [
            { "type" : "text", "text": "Generate a caption for this image in 50 words."},
            { "type" : "image_url", "image_url" : {"url": "https://images.pexels.com/photos/7683821/pexels-photo-7683821.jpeg"} }
        ]
    }]
)

print(response.choices[0].message.content)