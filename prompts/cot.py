from openai import OpenAI
from dotenv import load_dotenv
import os
import json 


load_dotenv()

# client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"), 
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

client = OpenAI()


SYSTEM_PROMPT = f"""
    You're an expert AI assistant in resolving user queries using chain of thought reasoning.
    You work on START, PLAN, OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, then finally give out the OUTPUT.

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
    {{'step': 'START' | 'PLAN' | 'OUTPUT', 'content': 'string'}}

    Example:
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
"""

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

USER_PROMPT = input("👋🏻:")

message_history.append({"role": "user", "content": USER_PROMPT})

# Chain of Thought Prompting - The model is given a question or task and is asked to think step by step.
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

    if parsed_response.get('step') == "OUTPUT":
        print("🤖", parsed_response.get('content')) 
        break
