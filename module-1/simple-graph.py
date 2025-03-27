from typing_extensions import TypedDict
import random
from typing import Literal

from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

# define the state of the graph
class State(TypedDict):
    graph_state:str

# define the nodes of the graph

def node_1(state):
    return {"graph_state": state['graph_state'] +" I am "}

def node_2(state):
    return {"graph_state": state['graph_state'] + "happpy!"}

def node_3(state):
    return {"graph_state": state['graph_state'] + "sad"}

# define edges of the graph

def decide_mood(state) -> Literal["node_2", "node_3"]:
    if random.random() < 0.5:
        return "node_2"
    return "node_3"

# build the graph
builder = StateGraph(State)
builder.add_node("node_1",node_1)
builder.add_node("node_2",node_2)
builder.add_node("node_3",node_3)

# build the edges
builder.add_edge(START,"node_1")
builder.add_conditional_edges("node_1",decide_mood)
builder.add_edge("node_2",END)
builder.add_edge("node_3",END)

# add
graph = builder.compile()

result = graph.invoke({"graph_state": "Hello, I am Anurag."})
print(result)





