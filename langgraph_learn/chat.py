from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    print("\nInside chatbot node", state)
    return {"messages": ["hey there! This is a message from chatbot!"]}


def samplenode(state: State):
    print("\nInside samplenode node", state)
    return {"messages": ["Sample Node message appended."]}


graph_builder = StateGraph(State)
# state : {"messages": ["Hello World!"]}
graph_builder.add_node("chatbot", chatbot)
# state : {"messages": ["Hello World!", "hey there! This is a message from chatbot!"]}
graph_builder.add_node("samplenode", samplenode)
# state : {"messages": ["Hello World!", "hey there! This is a message from chatbot!", "Sample Node message appended."]}

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)
# (START) -> chatbot -> samplenode -> (END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": ["Hi, My name is Tarique"]}))

print("\nupdated_state", updated_state)