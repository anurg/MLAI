from typing_extensions import TypedDict
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

class OverallState(TypedDict):
    foo : int
class PrivateState(TypedDict):
    bar: int

def node_1(state:OverallState) -> PrivateState:
    return {"bar" : state["foo"] + 1}

def node_2(state:PrivateState) -> OverallState:
    return {"foo": state["bar"] + 1}

builder = StateGraph(OverallState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)


graph = builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))


result =graph.invoke({"foo" : 1})

print(result)