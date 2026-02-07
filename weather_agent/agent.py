from openai import OpenAI
from dotenv import load_dotenv
import json 
import requests


def get_weather(city: str):
    url = f"https://www.wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"


load_dotenv()

client = OpenAI()


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

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

USER_PROMPT = input("👋🏻:")

message_history.append({"role": "user", "content": USER_PROMPT})

available_tools = {"get_weather": get_weather}


while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        response_format={"type": "json_object"},
        messages=message_history
    )
        
    raw_response = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_response})

    parsed_response = json.loads(raw_response)    


    if parsed_response.get('step') == "START":
        print("🔥", parsed_response.get('content')) 
        continue

    if parsed_response.get('step') == "PLAN":
        print("🧠", parsed_response.get('content')) 
        continue

    if parsed_response.get('step') == "TOOL":
        tool_to_be_called = parsed_response.get('tool')
        tool_input = parsed_response.get('input')
        print(f"🛠️ {tool_to_be_called}({tool_input})")
        
        tool_response = available_tools[tool_to_be_called](tool_input)
        message_history.append({
            "role": "developer",
            "content": json.dumps({"step": "OBSERVE", "tool": tool_to_be_called, "input": tool_input, "output": tool_response})
        })
        continue

    if parsed_response.get('step') == "OUTPUT":
        print("🤖", parsed_response.get('content')) 
        break
