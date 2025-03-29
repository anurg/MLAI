from typing import TypedDict
from typing import Literal
import random
from dataclasses import dataclass
from pydantic import BaseModel, ValidationError, field_validator
# class TypedDictState(TypedDict):
#     name : str
#     mood : Literal["happy", "sad"]

# @dataclass
# class DataClassState:
#     name : str
#     mood : Literal["happy", "sad"]

class PydanticState(BaseModel):
    name : str
    mood : str  # 'happy' or 'sad'

    @field_validator('mood')
    @classmethod
    def validate_mood(cls, value):
        if value not in ["happy", "sad"]:
            raise ValueError("mood must be either happy or sad")
        return value

# try:
#     state = PydanticState(name="Anurag", mood="mad")
# except ValidationError as e:
#     print("Validation error:", e)



from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

def node_1(state):
    # return {"name" : state["name"] + " is ...."}
    return {"name" : state.name + " is ...."}

def node_2(state):
    return {"mood" : "happy"}

def node_3(state):
    return {"mood" : "sad"}

def decide_mood(state) -> Literal["node_2", "node_3"]:
    if random.random() < 0.5:
        return "node_2"
    return "node_3"


    
# builder = StateGraph(TypedDictState)
# builder = StateGraph(DataClassState)
builder = StateGraph(PydanticState)

builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

# result = graph.invoke({"name" : "Anurag"})
# result = graph.invoke(DataClassState(name= "Anurag", mood="mad"))
state = PydanticState(name= "Anurag", mood="sad")
result = graph.invoke(state)
print(result)


