from typing_extensions import TypedDict
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

class OverallState(TypedDict):
    question : str
    answer : str
    notes  : str

class InputState(TypedDict):
    question : str

class OutputState(TypedDict):
    answer : str

  
    


def thinking_code(state:InputState):
    return {"answer" : "Bye", "notes" : "His name is Lance"}

def answering_node(state:OverallState) -> OutputState:
    return {"answer" : "Bye Lance"}

builder = StateGraph(OverallState, input = InputState, output=OutputState)
builder.add_node("node_1", thinking_code)
builder.add_node("node_2", answering_node)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)


graph = builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))


result =graph.invoke({"question" : "Hello"})

print(result)