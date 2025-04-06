from dotenv import load_dotenv
from typing import TypedDict
from langgraph.errors import NodeInterrupt
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from pprint import pprint

load_dotenv()

class State(TypedDict):
    input:str

def node_1(state:State) -> State:
    print("--- node_1 ---")
    return state

def node_2(state:State) -> State:
    if len(state["input"])>5:
        raise NodeInterrupt(f"Recieved Input that is longer than 5 characters: {state['input']}")
    print("--- node_2 ---")
    return state

def node_3(state:State) -> State:
    print("--- node_3 ---")
    return state

builder = StateGraph(State)
builder.add_node("node_1",node_1)
builder.add_node("node_2",node_2)
builder.add_node("node_3",node_3)

builder.add_edge(START,"node_1")
builder.add_edge("node_1","node_2")
builder.add_edge("node_2","node_3")
builder.add_edge("node_3",END)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

config = {"configurable" : {"thread_id" : "1"}}

input_message = HumanMessage(content="Hello World!")

try:
    for event in graph.stream(input_message,config,stream_mode="values"):
        print(event)
except KeyError as e:
    print(e)

current_state=graph.get_state(config)
print(current_state.tasks)

graph.update_state(config, {"input" : "Hello"})
for event in graph.stream(None,config,stream_mode="values"):
    print(event["input"])


