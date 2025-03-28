from pprint import pprint
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage,AnyMessage
import os
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
#  Add dotenv for loading OPENAI_API_KEY
import dotenv
dotenv.load_dotenv()

messages = [AIMessage(content="So You said you are researching ocean mammals", name="Model")]
messages.append(HumanMessage(content="Yeah, that's right.",name="Lance"))
messages.append(AIMessage(content="Great, so what would you like  to learn about!",name="Model"))
messages.append(HumanMessage(content="I would like to learn about the best places to see Orca in India",name="Lance"))

# for m in messages:
#     m.pretty_print()

# print(os.environ.get("OPENAI_API_KEY"))

llm = ChatOpenAI(model="gpt-4o")
# result = llm.invoke(messages)
# print(type(result))
# result.pretty_print()

# define tool and bind with llm
def multiply(a: int, b: int) -> int:
    """
    Multiply a and b
    Args:
        a: first int
        b: second int
    """
    return a * b

llm_with_tools = llm.bind_tools([multiply])

# tool_call = llm_with_tools.invoke([HumanMessage(content="What is 23 multiplied by 2", name="Lance")])
# tool_call.pretty_print()

class MessagesState(MessagesState):
    pass

# initial_messages=[AIMessage(content="Hello, How can I assist you?",name="Model"),
#                   HumanMessage(content="I am looking for information on Marine Biology",name="Lance")]

# new_message=AIMessage(content="Sure,I can help you with that. What speciality are you interested in?", name="Model")
# messages=add_messages(initial_messages,new_message)
# for m in messages:
#     m.pretty_print()

from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

# Node
def tool_calling_llm(state:MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm",END)
graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

# messages = graph.invoke({"messages" : HumanMessage(content="Hello")})
messages = graph.invoke({"messages" : HumanMessage(content="multiply 22 with 2")})

for m in messages['messages']:
    m.pretty_print()

