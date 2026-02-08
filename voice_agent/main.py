from dotenv import load_dotenv 
from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer

import asyncio
import speech_recognition as sr


load_dotenv()

client = OpenAI()
async_client = AsyncOpenAI()


async def text_to_speech(text: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="Speak in a cheerful and positive tone.",
        input=text,
        response_format="pcm"
    ) as response:
        await LocalAudioPlayer().play(response)


def main():
    r = sr.Recognizer()

    with sr.Microphone() as source:  
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2

        SYSTEM_PROMPT = """
            You are an expert voice agent. You are given the transcript of what 
            user has said in voice.
            You need to output as if you are a voice agent and whatever you speak
            will be converted back to audio using AI and played back to user.
        """
        
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        while True:
            print("Speak something...")
            audio = r.listen(source)

            print("Processing audio...")
            stt = r.recognize_google(audio)

            print("You said: ", stt)
            
            messages.append({"role": "user", "content": stt})

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages
            )
            text = response.choices[0].message.content
            print("AI response: ", text)
            
            asyncio.run(text_to_speech(text=text))


main()