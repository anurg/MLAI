from langgraph.graph import StateGraph, START,END
from typing import TypedDict, Any, Annotated
from IPython.display import Image,display
from operator import add
from langgraph.errors import InvalidUpdateError 


def sorting(left,right):
    if not isinstance(left,list):
        left = [left]
    if not isinstance(right,list):
        right = [right]
    sorted_list = sorted(left + right , reverse=False)
    return sorted_list
class State(TypedDict):
    state:Annotated[list,sorting]

class ReturnNodeValue:
    def __init__(self,node_secret:str):
        self._value = node_secret
    def __call__(self, state:State) -> Any:
        print(f"Adding {self._value} to {state['state']}")
        return {"state" : [self._value]}

builder = StateGraph(State)
builder.add_node("a", ReturnNodeValue("I am A"))
builder.add_node("b", ReturnNodeValue("I am B"))
builder.add_node("b2", ReturnNodeValue("I am B2"))
builder.add_node("c", ReturnNodeValue("I am C"))
builder.add_node("d", ReturnNodeValue("I am D"))

builder.add_edge(START,"a")
builder.add_edge("a","b")
builder.add_edge("b","b2")
builder.add_edge("a","c")
builder.add_edge(["c","b2"],"d")
builder.add_edge("d",END)

graph = builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))
try:
    response=graph.invoke({"state":[]})
    print(response)
except InvalidUpdateError as e:
    print(e)
        
        