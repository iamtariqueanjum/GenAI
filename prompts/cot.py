from openai import OpenAI
from dotenv import load_dotenv
import os
import json 


load_dotenv()

client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = f"""
    You're an expert AI assistant in resolving user queries using chain of thought reasoning.
    You work on START, PLAN, OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, then finally give out the OUTPUT.

    Rules:
    - Strictly follow the given JSON format output.
    - Only run one step at a time.
    - The sequence of steps is START (where user gives input), PLAN (that can be multiple times) and finally give the OUTPUT(which is displayed to the user)

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



USER_PROMPT = "Hey, Write code to add two numbers as fast as possible using cache in js?"

# Chain of Thought Prompting - The model is given a question or task and is asked to think step by step.
response = client.chat.completions.create(
    model="gemini-3-flash-preview", 
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT}, 
        {"role": "user", "content": USER_PROMPT},
        {"role": "assistant", "content": json.dumps({"step": "PLAN", "content": "The user wants an optimized JavaScript function to add two numbers using a caching mechanism to improve performance for repeated calculations."})},
        {"role": "assistant", "content": json.dumps({"step": "PLAN", "content": "I will create a function that uses a Map object to store the results of addition operations, allowing for O(1) retrieval of previously calculated sums."})}
    ])
print(response.choices[0].message.content)