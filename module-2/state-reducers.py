from typing_extensions import TypedDict
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from typing import Annotated
from operator import add
# define the state of the graph
class State(TypedDict):
    foo : Annotated[list[int], add]
    # foo : int

def node_1(state):
    return {"foo" : [state["foo"][-1] + 1]}
    # return {"foo" : state["foo"] + 1}

def node_2(state):
    return {"foo" : [state["foo"][-1] + 1]}
    # return {"foo" : state["foo"] + 1}

def node_3(state):
    return {"foo" : [state["foo"][-1] + 1]}
    # return {"foo" : state["foo"] + 1}


builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_1", "node_3")
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

from langgraph.errors import InvalidUpdateError
# result = graph.invoke({"foo" : [1]})
try:
    result = graph.invoke({"foo" : [1]})
    print(result)
except InvalidUpdateError as e:
    print(e)

try:
    result = graph.invoke({"foo" : None})

except TypeError as e:
    print(e)

