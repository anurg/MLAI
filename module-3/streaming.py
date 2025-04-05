import dotenv
from langchain_core.messages import HumanMessage,RemoveMessage
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import MessagesState
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image, display
from pprint import pprint
import asyncio

dotenv.load_dotenv()
class State(MessagesState):
    summary:str

llm=ChatOpenAI(model="gpt-4o", temperature=0)

def call_model(state):
    summary = state.get("summary","")
    if summary:
        summary_message=f"Here is the summary of converstaion till now {summary}"
        messages= state["messages"] + [HumanMessage(content=summary_message)]
    else:
        messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages":response}

def summarize(state):
    # check if summary is empty or not. If not empty, add the previous summary message
    summary = state.get("summary","")
    if summary:
        summary_message = (
            f"Here is the summary of the converstaion till now {summary} \n\n"
            "Extend the summary by summarizing messages above"
        )
    else:
        summary_message = f"Extend the summary by summarizing messages above"
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = llm.invoke(messages)

    # Delete the chain of old messages and return
    delete_messages = [RemoveMessage(id=m.id) for m in state[messages][:-2]]
    return {"summary" : response.content,"messages":delete_messages}

def should_continue(state):
    messages = state["messages"]
    if len(messages) > 6:
        return "summarize"
    return END

builder = StateGraph(MessagesState)
builder.add_node("call_model",call_model)
builder.add_node("summarize",summarize)

builder.add_edge(START,"call_model")
builder.add_conditional_edges("call_model",should_continue)
builder.add_edge("summarize",END)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

display(Image(graph.get_graph().draw_mermaid_png()))

# config = {"configurable" : {"thread_id" : "1"}}

# input_message=HumanMessage(content="Hello , I am Lance")
# for chunk in graph.stream({"messages" : [input_message]},config, stream_mode="updates"):
#     chunk["call_model"]["messages"].pretty_print()

# config = {"configurable" : {"thread_id" : "2"}}

# input_message=HumanMessage(content="Hello , I am Lance")
# for chunk in graph.stream({"messages" : [input_message]},config, stream_mode="values"):
#     for m in chunk["messages"]:
#         m.pretty_print()

config = {"configurable" : {"thread_id" : "2"}}

input_message=HumanMessage(content="Tell me about 49ers NFL Team")
node_to_stream = "call_model"
async def stream_graph_events(input_message):
    async for event in graph.astream_events({"messages": [input_message]}, config, version="v2"):
          if event["event"] == "on_chat_model_stream" and event['metadata'].get('langgraph_node','') == node_to_stream:
            data=event["data"]
            print(data["chunk"].content, end="|")

if __name__ == "__main__":
    asyncio.run(stream_graph_events(input_message))