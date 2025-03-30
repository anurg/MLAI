from pprint import pprint
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import MessagesState
from langchain_core.messages import RemoveMessage
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
import os

import dotenv
dotenv.load_dotenv()
# print(os.getenv('OPENAI_API_KEY'))



# for m in messages:
#     m.pretty_print()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")
# result = llm.invoke(messages)
# result.pretty_print()

# Nodes
def filter_messages(state: MessagesState):
    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"messages": delete_messages}

def llm_node(state:MessagesState):
    return {"messages" : [llm.invoke(state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("filter_messages", filter_messages)
builder.add_node("llm_node", llm_node)
builder.add_edge(START, "filter_messages")
builder.add_edge("filter_messages", "llm_node")
builder.add_edge("llm_node", END)

graph = builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))


# Message list with a preamble
messages = [AIMessage("Hi.", name="Bot", id="1")]
messages.append(HumanMessage("Hi.", name="Lance", id="2"))
messages.append(AIMessage("So you said you were researching ocean mammals?", name="Bot", id="3"))
messages.append(HumanMessage("Yes, I know about whales. But what others should I learn about?", name="Lance", id="4"))

# Invoke
output = graph.invoke({'messages': messages})
for m in output['messages']:
    m.pretty_print()

