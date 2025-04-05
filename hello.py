import dotenv
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage,RemoveMessage
from langchain_openai import ChatOpenAI
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.checkpoint.memory import MemorySaver
from pprint import pprint

dotenv.load_dotenv()

class State(MessagesState):
    summary: str

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def call_node(state):
    # check if summary is present, add it as System prompt
    summary = state.get("summary","")
    if summary :
        system_message=f"Here is the summary of past messages {summary}" 
        messages= [SystemMessage(content=system_message)] + state["messages"]
    else:
        messages = state["messages"]
    return {"messages" : [llm.invoke(messages)] }

def summarize(state):
    # summarize the message and add to existing summary or initialize summary
    summary = state.get("summary","")
    if summary:
        system_message=f"Here is the summary of past messages {summary} \n\n"
                        "Add the summary of above messages in existing summary"
    else:
        system_message=f"Add the summary of above messages in summary"

    messages = [SystemMessage(content=system_message)] + state["messages"]
    response = llm.invoke(messages)
    # delete old messages from State except last 2
    remove_messages=[RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"messages" :remove_messages, "summary" : response.content}

def conditional_route(state):
    # check for no of messages in state, if greater than 5 then route to summarize.
    messages = state.get("messages","")
    if len(messages)>5:
        return "summarize"
    return END


builder = StateGraph(State)
builder.add_node("call_node", call_node)
builder.add_node("summarize",summarize)

builder.add_edge(START,"call_node")
builder.add_conditional_edges("conditional_route", conditional_route)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

config={"configurable" : {"thread_id" : "1"}}
messages=[HumanMessage(content="Hello I am Lance")]
response = graph.invoke({"messages" : messages}, config=config)
for m in response["messages"]:
    m.pretty_print()

messages=[HumanMessage(content="Whats my name?")]
response = graph.invoke({"messages" : messages}, config=config)
for m in response["messages"]:
    m.pretty_print()   