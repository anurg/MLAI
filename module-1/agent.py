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
# define tools
def multiply(a:int,b:int) -> int:
    """
    multiply two numbers a and b
    Args:
        a : first integer
        b : second integer
    """
    return a * b
def add(a:int,b:int) -> int:
    """
    add two numbers a and b
    Args:
        a : first integer
        b : second integer
    """
    return a + b
def subtract(a:int,b:int) -> int:
    """
    subtract two numbers a and b
    Args:
        a : first integer
        b : second integer
    """
    return a - b
def divide(a:int,b:int) -> int:
    """
    divide two numbers a and b
    Args:
        a : first integer
        b : second integer
    """
    return a / b
# define tools
tools = [multiply, add, subtract, divide]
# bind tool to llm
llm_with_tools = llm.bind_tools(tools,parallel_tool_calls=False)

# define node (llm)
def assistant(state:MessagesState):
    return {"messages" : [llm_with_tools.invoke(state["messages"])]}
# define graph & node & edges
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
# Add tools node
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")
builder.add_edge("tools", END)
graph = builder.compile()
# display graph
from IPython.display import Image, display
# display(Image(graph.get_graph().draw_mermaid_png()))
# invoke graph with State

result = graph.invoke({"messages" : [HumanMessage(content="Add 4 and 4. Multiply the output by 2. Divide the output by 4 Then subtract 1 from output.",name="Anurag")]})

# pretty print messages
for m in result["messages"]:
    m.pretty_print()
