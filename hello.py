from pprint import pprint
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage,AIMessage, SystemMessage, AnyMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START,END,StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

def multiply(a:int, b:int) -> int:
    """ mutiply two integers
        a: first integer
        b: second integer
    """
    return a * b
def add(a:int, b:int) -> int:
    """ add two integers
        a: first integer
        b: second integer
    """
    return a + b
def subtract(a:int, b:int) -> int:
    """ Subtract two integers
        a: first integer
        b: second integer
    """
    return a - b
tools = [multiply]
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools=llm.bind_tools(tools)
def tool_calling_llm(state:MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm",tool_calling_llm)
builder.add_node("tools",ToolNode(tools))

builder.add_edge(START,"tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm",tools_condition)
builder.add_edge("tools","tool_calling_llm")

graph = builder.compile()

response = graph.invoke({"messages" : HumanMessage(content="Multiply 2 and 3. Then add 4 to it. Then subtract 1 from it.")})

for m in response["messages"]:
    m.pretty_print()


