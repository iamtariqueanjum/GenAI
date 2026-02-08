import json 
import os
import requests

import asyncio
import speech_recognition as sr

from openai import OpenAI, AsyncOpenAI
from openai.helpers import LocalAudioPlayer

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional


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


def run_cmd(cmd: str):
    response = os.system(cmd)
    return response


def get_weather(city: str):
    url = f"https://www.wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"

available_tools = {"get_weather": get_weather, "run_cmd": run_cmd}


SYSTEM_PROMPT = f"""
    You're an expert AI assistant in resolving user queries using chain of thought reasoning.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, then finally give out the OUTPUT.
    You can also call a tool if required from the list of available tools.
    For every tool call wait for the OBSERVE step which is the output from the called tool.
    
    Rules:
    - Strictly follow the given JSON format output.
    - Only run one step at a time.
    - The sequence of steps is START (where user gives input), PLAN (that can be multiple times) and finally give the OUTPUT(which is displayed to the user)
    - You must output EXACTLY ONE JSON object per response.
    - Never output multiple steps at once.
    - Do NOT explain hidden reasoning.
    - Each response must be one of:
        START → PLAN → PLAN → ... → OUTPUT
    - After emitting a step, STOP.

    Output JSON format:
    {{'step': 'START' | 'PLAN' | 'OUTPUT' | 'TOOL', 'content': 'string'}}

    Available Tools:
    - get_weather(city: str): Takes city name as input string and returns the weather info about the city.
    - run_cmd(cmd: str): Takes linux sytem command  as input string and executes the command on users system and returns the output from that command. 
    
    Example 1:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN : {{"step": "PLAN", "content": "Seems like user is interested in math problem"}}
    PLAN : {{"step": "PLAN", "content": "looking at the problem, We should use BODMAS rule here."}}
    PLAN : {{"step": "PLAN", "content": "YES, BODMAS is correct choice here"}}
    PLAN : {{"step": "PLAN", "content": "first we multiply 3 * 5 which is 15"}}
    PLAN : {{"step": "PLAN", "content": "then, the equation becomes 2 + 15 / 10"}}
    PLAN : {{"step": "PLAN", "content": "now, we perform division 15/10 which is 1.5"}}
    PLAN : {{"step": "PLAN", "content": "Now, the equation becomes 2 + 1.5"}}
    PLAN : {{"step": "PLAN", "content": "Let's add the equation to result in 3.5"}}
    PLAN : {{"step": "PLAN", "content": "Finally, we have solved the problem we are left with 3.5 as answer"}}
    OUTPUT : {{"step": "OUTPUT", "content": "3.5"}}

    Example 2:
    START: What is the current weather in Delhi?
    PLAN : {{"step": "PLAN", "content": "Seems like user is interested in weather of Delhi"}}
    PLAN : {{"step": "PLAN", "content": "Lets see if there are any available tool from list of available tools"}}
    PLAN : {{"step": "PLAN", "content": "Great, we have get_weather tool available for this query"}}
    PLAN : {{"step": "PLAN", "content": "I need to call get_weather tool for delhi input for city"}}
    PLAN : {{"step": "TOOL", "tool": "get_weather", "input": "Delhi"}}
    PLAN : {{"step": "OBSERVE", "tool": "get_weather", "output": "The temperature of delhi is cloud 20 C"}}
    PLAN : {{"step": "PLAN", "content": "Great, I got the weather info about Delhi"}}
    OUTPUT : {{"step": "OUTPUT", "content": "The current weather in Delhi is 20 C with some cloudy sky."}}


"""

class OutputFormat(BaseModel):
    step : str = Field(..., description="The ID of the step. Example : PLAN, TOOL, OUTPUT etc")
    content: Optional[str] = Field(None, description="The optional string content of the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call")
    input: Optional[str] = Field(None, description="The input of the tool")


message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

r = sr.Recognizer()
with sr.Microphone() as source:  
    r.adjust_for_ambient_noise(source)
    r.pause_threshold = 2

    while True:
        print("Speak something...")
        audio = r.listen(source)

        USER_PROMPT = r.recognize_google(audio)

        message_history.append({"role": "user", "content": USER_PROMPT})

        while True:
            response = client.chat.completions.parse(
                model="gpt-4o-mini", 
                response_format=OutputFormat,
                messages=message_history
            )
                
            raw_response = response.choices[0].message.content
            
            message_history.append({"role": "assistant", "content": raw_response})

            parsed_response = response.choices[0].message.parsed


            if parsed_response.step == "START":
                print("🔥", parsed_response.content) 
                continue

            if parsed_response.step == "PLAN":
                print("🧠", parsed_response.content) 
                continue

            if parsed_response.step == "TOOL":
                tool_to_be_called = parsed_response.tool
                tool_input = parsed_response.input
                print(f"🛠️ {tool_to_be_called}({tool_input})")
                
                tool_response = available_tools[tool_to_be_called](tool_input)
                message_history.append({
                    "role": "developer",
                    "content": json.dumps({"step": "OBSERVE", "tool": tool_to_be_called, "input": tool_input, "output": tool_response})
                })
                continue

            if parsed_response.step == "OUTPUT":
                print("🤖", parsed_response.content) 
                asyncio.run(text_to_speech(parsed_response.content))
