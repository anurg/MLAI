# Open AI key & langsmith key
import os
import dotenv
dotenv.load_dotenv()
from pprint import pprint
# # check keys are loaded
# print("OPENAI_API_KEY = ", os.getenv("OPENAI_API_KEY"))
# print("LANGSCHAIN_API_KEY = ",os.getenv("LANGCHAIN_API_KEY"))
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "langchain-academy"

# define llm
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")

#  define state (MessagesState)
from langchain_core.messages import  RemoveMessage, HumanMessage, SystemMessage
from langgraph.graph import MessagesState
class State(MessagesState):
    summary: str

# define call_model node, which will first check if summary is empty or not. If not epmpty, it will create a SystemMessage with content
# "Here is the summary of the converstaion so far: {summary}" and then call llm with the system message
#  if summary is empty, it will call llm with the messages in the state

from langgraph.graph import StateGraph,START,END
from IPython.display import Image, display

# Node
def call_model(state:State):
    summary = state.get("summary","")
    if summary:
        sys_message = SystemMessage(content=f"Here is the summary of the conversation so far: {summary}", name="System")
        messages = [sys_message] + state["messages"]
        
    else:
        messages = state["messages"]
    result = llm.invoke(messages)
    return {"messages" : [result]}

#  define node for summarization
def summarize(state:State):
    summary = state.get("summary","")
    if summary:
        summary_message = (f"Here is the summary of the conversation so far: {summary} /n/n"
                          "Extend the summary by taking into account previous messages")
    else:
        summary_message = "Create a summary of the conversation so far"
    
    #  Add the summary_message to messages
    messages = state["messages"] + [HumanMessage(content=summary_message, name="User")]
    response = llm.invoke(messages)

    #  Once summary is generated, remove all but last 2 messages from the state and update the summary
    delete_message = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary" : response.content, "messages" : delete_message }

# define conditional edge
def condition(state:State):
    """
    return the next node to go
    """
    if len(state["messages"]) > 6:
        return "summarize"
    return END

#  Add memory in Graph
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()


# define graph
builder = StateGraph(State)
builder.add_node("call_model", call_model)
builder.add_node("summarize", summarize)
builder.add_edge(START, "call_model")
builder.add_conditional_edges("call_model", condition)
graph = builder.compile(checkpointer=memory)
display(Image(graph.get_graph().draw_mermaid_png))

config = {"configurable" : {"thread_id" : "1"}}

# start conversation with memory

input_message = HumanMessage(content="Hi, I am Lance.", name="Lance")
result = graph.invoke({"messages" : [input_message]}, config)
for m in result["messages"][-1:]:
    m.pretty_print()

input_message = HumanMessage(content="What is my name?", name="Lance")
result = graph.invoke({"messages" : [input_message]}, config)
for m in result["messages"][-1:]:
    m.pretty_print()

input_message = HumanMessage(content="I like 49ers.", name="Lance")
result = graph.invoke({"messages" : [input_message]}, config)
for m in result["messages"][-1:]:
    m.pretty_print()


input_message = HumanMessage(content="i like Nick Bosa, isn't he the highest paid defensive player?")
output = graph.invoke({"messages": [input_message]}, config) 
for m in output['messages'][-1:]:
    m.pretty_print()


summary = graph.get_state(config).values.get("summary","")
print(summary)