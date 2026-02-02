from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()
client = Client(
    host="http://localhost:11434"   
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/contact")
async def contact():
    return {"email": "tarique@gmail.com"}

@app.post("/chat")
async def chat_with_ollama(message: str = Body()):
    response = client.chat(
        model="gemma:2b",
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return {"response": response.message.content}
