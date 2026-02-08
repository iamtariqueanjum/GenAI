from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from openai import OpenAI
from typing_extensions import TypedDict
from typing import Optional, Literal


load_dotenv()

client = OpenAI()


class State(TypedDict):
    user_query : str
    llm_output: Optional[str]
    is_good: Optional[bool]


def chatbot(state: State):
    print("\n\nInside chatbot node", state)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": state.get("user_query")}
        ]
    )
    state["llm_output"] = response.choices[0].message.content
    state["is_good"] = True # True or False
    return state


def evaluate_response(state: State) -> Literal["advanced_chatbot", "end_node"]:
    print("\n\nEvaluating response...", state)
    if not state.get('is_good'):
        return "advanced_chatbot"
    return "end_node"


def advanced_chatbot(state: State):
    print("\n\nInside advanced chatbot node", state)
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": state.get("user_query")}
        ]
    )
    state["llm_output"] = response.choices[0].message.content
    return state


def end_node(state: State):
    return state


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("evaluate_response", evaluate_response)
graph_builder.add_node("advanced_chatbot", advanced_chatbot)
graph_builder.add_node("end_node", end_node)


graph_builder.add_edge(START, "chatbot")

graph_builder.add_conditional_edges("chatbot", evaluate_response)

graph_builder.add_edge("advanced_chatbot", "end_node")
graph_builder.add_edge("end_node", END)


graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "What is 2 + 2?"}))
print(updated_state)