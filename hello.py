import dotenv
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage,RemoveMessage
from langchain_openai import ChatOpenAI
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.checkpoint.memory import MemorySaver
from pprint import pprint
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

dotenv.load_dotenv()
db_path = "example.db"
conn = sqlite3.connect(db_path, check_same_thread=False)

class State(MessagesState):
    summary: str

llm = ChatOpenAI(model="gpt-4o")

def call_node(state):
    # check if summary is present, add it as System prompt
    summary = state.get("summary","")
    if summary :
        summary_message=f"Summary of conversation earlier: {summary}"
        messages=  [HumanMessage(content=summary_message)] + state["messages"]
    else:
        messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": response}

def summarize(state):
    # summarize the message and add to existing summary or initialize summary
    summary = state.get("summary","")
    if summary:
        summary_message = ( 
                        f"This is summary of the conversation to date: {summary}\n\n"
                        "Extend the summary by taking into account the new messages above:"
        )
    else:
        summary_message=f"Create a summary of the conversation above:"

    messages =    state["messages"] + [HumanMessage(content=summary_message)] 
    response = llm.invoke(messages)
    # delete old messages from State except last 2
    remove_messages=[RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary" : response.content, "messages" :remove_messages}

def conditional_route(state):
    # check for no of messages in state, if greater than 5 then route to summarize.
    """Return the next node to execute."""
    messages = state["messages"]
    if len(messages)>5:
        return "summarize"
    return END


builder = StateGraph(State)
builder.add_node("call_node", call_node)
builder.add_node("summarize",summarize)

builder.add_edge(START,"call_node")
builder.add_conditional_edges("call_node",conditional_route )
builder.add_edge("summarize",END)

# memory = MemorySaver()
memory = SqliteSaver(conn)
graph = builder.compile(checkpointer=memory)
# display(Image(graph.get_graph().draw_mermaid_png()))


# Create a thread
config = {"configurable": {"thread_id": "1"}}
# config = {"configurable": {"thread_id": "2"}}

# # Start conversation
# input_message = HumanMessage(content="hi! I'm Lance")
# output = graph.invoke({"messages": [input_message]}, config) 
# for m in output['messages'][-1:]:
#     m.pretty_print()

# input_message = HumanMessage(content="what's my name?")
# output = graph.invoke({"messages": [input_message]}, config) 
# for m in output['messages'][-1:]:
#     m.pretty_print()

# input_message = HumanMessage(content="i like the 49ers!")
# output = graph.invoke({"messages": [input_message]}, config) 
# for m in output['messages'][-1:]:
#     m.pretty_print()

# input_message = HumanMessage(content="i like Nick Bosa, isn't he the highest paid defensive player?")
# output = graph.invoke({"messages": [input_message]}, config) 
# for m in output['messages'][-1:]:
#     m.pretty_print()

print(graph.get_state(config).values.get("summary",""))