import getpass
import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from IPython.display import Image, display


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

def _set_env(var : str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("ANTHROPIC_API_KEY")

def chatbot(state: State):
    return { 
        "messages": [
            llm.invoke(state["messages"])
        ]
    }

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)




llm = ChatAnthropic(model="claude-3-5-sonnet-20240620") 

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

# try:
#     mermaid_markup = graph.get_graph().draw_mermaid()
#     with open("graph.mmd", "w") as f:
#         f.write(mermaid_markup)
# except Exception as e:
#     print(e)


stream_graph_updates("hello how are you?")
stream_graph_updates("is langchains langgraph module part of your training data?")
stream_graph_updates("tell me all you know about it")

# while True:
#     try:
#         user_input = input("You: ")
#         print(f"user input is {user_input}")
#         if user_input.lower() in  ["exit", "quit", "bye"]:
#             print("Goodbye!")
#             break
#         stream_graph_updates(user_input)
#     except Exception as e:
#         print(f"error is {e}")
#         break
