# load OPENAI_API_KEY
from pprint import pprint
import os
import dotenv
dotenv.load_dotenv()
# print OPENAI_API_KEY
# print(os.getenv("OPENAI_API_KEY"))
# define state (MessagesState)
from langgraph.graph import MessagesState
class MessagesState(MessagesState):
    pass
# iinitialize llm
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")
# import HumanMessage
from langchain_core.messages import HumanMessage
# result = llm.invoke([HumanMessage(content="Hello World!",name="Anurag")])
# result.pretty_print()
# define tool
def multiply(a:int,b:int) -> int:
    """
    multiply two numbers a and b
    Args:
        a : first integer
        b : second integer
    """
    return a * b
# bind tool to llm
llm_with_tools = llm.bind_tools([multiply])

# define node (llm)
def tool_calling_llm(state:MessagesState):
    return {"messages" : [llm_with_tools.invoke(state["messages"])]}
# define graph & node & edges
from langgraph.graph import StateGraph, START, END

builder = StateGraph(MessagesState)
builder.add_node("llm_with_tools", tool_calling_llm)
builder.add_edge(START, "llm_with_tools")

builder.add_edge("llm_with_tools", END)
graph = builder.compile()
# display graph
from IPython.display import Image, display
# display(Image(graph.get_graph().draw_mermaid_png()))
# invoke graph with State

result = graph.invoke({"messages" : [HumanMessage(content="Multiply 2 with 3",name="Anurag")]})

# pretty print messages
for m in result["messages"]:
    m.pretty_print()
