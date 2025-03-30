from pprint import pprint
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import MessagesState
from langchain_core.messages import RemoveMessage, trim_messages
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
import os

import dotenv
dotenv.load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "langchain-academy"

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")

# Nodes
def llm_node(state:MessagesState):
    # messages = trim_messages(
    #     state["messages"],
    #     max_tokens=100,
    #     strategy="last",
    #     token_counter=ChatOpenAI(model="gpt-4o").,
    #     allow_partial=False
    # )
    # return {"messages" : messages}
    return {"messages" : [llm.invoke(state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("llm_node", llm_node)
builder.add_edge(START, "llm_node")
builder.add_edge("llm_node", END)

graph = builder.compile()


# Message list with a preamble
messages = [AIMessage("Hi.", name="Bot", id="1")]
messages.append(HumanMessage("Hi.", name="Lance", id="2"))
messages.append(AIMessage("So you said you were researching ocean mammals?", name="Bot", id="3"))
messages.append(HumanMessage("Yes, I know about whales. But what others should I learn about?", name="Lance", id="4"))

# Invoke
output = graph.invoke({'messages': messages})

# messages.append(output['messages'][-1])
messages.append(HumanMessage(f"Tell me more about Narwhals!", name="Lance"))

output = graph.invoke({'messages': messages})
# for m in output['messages']:
#     m.pretty_print()


# messages.append(output['messages'][-1])
messages.append(HumanMessage(f"Tell me where Orcas live!", name="Lance"))
# Invoke


messages_out_trim = graph.invoke({'messages': messages})



