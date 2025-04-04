from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.errors import InvalidUpdateError
from IPython.display import Image, display
from operator import add

def custom_reducer(left:list|None,right:list|None) -> list:
    """Safely combine two lists, handling cases where either or both inputs might be None.

    Args:
        left (list | None): The first list to combine, or None.
        right (list | None): The second list to combine, or None.

    Returns:
        list: A new list containing all elements from both input lists.
               If an input is None, it's treated as an empty list.
    """
    if not left:
        left = []
    if not right:
        right = []
    return left + right
# class State(TypedDict):
#     num:int
class DefaultState(TypedDict):
    num:Annotated[list[int],add]

class CustomReducerState(TypedDict):
    num:Annotated[list[int],custom_reducer]



def node_1(state):
    return {"num" : None}
    # return {"num" : [state["num"][-1]+1]}

# def node_2(state):
#     return {"num" : [state["num"][-1]+1]}

# def node_3(state):
#     return {"num" : [state["num"][-1]+1]}

builder = StateGraph(CustomReducerState)
# builder = StateGraph(DefaultState)
builder.add_node("node_1", node_1)
# builder.add_node("node_2", node_2)
# builder.add_node("node_3", node_3)

builder.add_edge(START,"node_1")
builder.add_edge("node_1",END)
# builder.add_edge("node_1", "node_2")
# builder.add_edge("node_1", "node_3")

# builder.add_edge("node_2", END)
# builder.add_edge("node_3", END)


graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))
# try:
#     result = graph.invoke({"num":[1]})
#     print(result)
# except InvalidUpdateError as e:
#     print(e)
try:
    result = graph.invoke({"num":[2]})
    print(result)
except TypeError as e:
    print(e)