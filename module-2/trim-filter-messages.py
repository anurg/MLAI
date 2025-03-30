from pprint import pprint
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
import os

import dotenv
dotenv.load_dotenv()
# print(os.getenv('OPENAI_API_KEY'))

messages = [AIMessage(content="So you said, you are researching about Ocean mammals", name="Bot")]
messages.append(HumanMessage(content="Yeah,thats right.", name="Lance"))
messages.append(AIMessage(content="Great, so what would you like to learn about!", name="Bot"))
messages.append(HumanMessage(content="I would like to learn about the best places to see Orca in India", name="Lance"))

# for m in messages:
#     m.pretty_print()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")
# result = llm.invoke(messages)
# result.pretty_print()

def llm_node(state:MessagesState):
    return {"messages" : [llm.invoke(state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("llm_node", llm_node)
builder.add_edge(START, "llm_node")
builder.add_edge("llm_node", END)

graph = builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))

result = graph.invoke({"messages" : messages})
for m in result["messages"]:
    m.pretty_print()

