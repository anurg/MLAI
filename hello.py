from typing_extensions import TypedDict
import random
from typing import Literal
from dataclasses import dataclass
from pydantic import BaseModel, ValidationError, field_validator

from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

# define the state of the graph
# class State(TypedDict):
#     graph_state:str

# @dataclass
# class State:
#     name:str
#     mood:Literal["happy","sad"]

class State(BaseModel):
    name:str
    mood:str

    @field_validator("mood")
    @classmethod
    def validate_mood(cls, value):
        if value not in ["happy","sad"]:
            raise ValueError("Mood must be either 'happy' or 'sad'")
        return value
# try:
#     state = State(name="Anurag",mood="mad")
#     print(state)
# except ValidationError as e:
#     print(e)    
        

# define the nodes of the graph

def node_1(state):
    return {"name": state.name+" is ... "}

def node_2(state):
    return {"mood": "happpy!"}

def node_3(state):
    return {"mood":  "sad"}

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
try:
    result = graph.invoke(State(name="Anurag",mood="mad"))
    print(result)
except ValidationError as e:
    print(e)
    








