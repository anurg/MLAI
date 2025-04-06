from dotenv import load_dotenv
from langgraph.graph import StateGraph,START,END, MessagesState
from langchain_core.messages import HumanMessage
from IPython.display import display,Image
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
load_dotenv()

def multiply(a:int, b:int)->int:
    """ multiply two integers
    Args:
        a:first integer
        b:second integer
    """
    return a * b

def add(a:int, b:int)->int:
    """ add two integers
    Args:
        a:first integer
        b:second integer
    """
    return a + b

def subtract(a:int, b:int)->int:
    """ subtract two integers
    Args:
        a:first integer
        b:second integer
    """
    return a - b

def divide(a:int, b:int)->int:
    """ Divide two integers
    Args:
        a:first integer
        b:second integer
    """
    if b == 0 :
        return 0
    return a / b

tools = [multiply,add,subtract,divide]
llm =ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Define Nodes
def tool_calling_llm(state:MessagesState):
    return {"messages" : [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm",tool_calling_llm)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START,"tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm",tools_condition)
builder.add_edge("tools","tool_calling_llm")

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

config = {"configurable" : {"thread_id" : "2"}}
initial_input= [HumanMessage(content="Multiply 2 and 3")]

for event in graph.stream({"messages" : initial_input}, config, stream_mode="values"):
    # event["messages"][-1].pretty_print()
    pass

all_states = [state for state in graph.get_state_history(config)]
# print(len(all_states))
# # for i , state in enumerate(all_states):
# #     print(f"State: {i}")
# #     print(f"{state.metadata}")

# to_replay = all_states[-2]
# print(to_replay.config)
# print(to_replay.next)
# print(to_replay.values)

# for event in graph.stream(None,to_replay.config,stream_mode="values"):
#     event["messages"][-1].pretty_print()

# all_states = [state for state in graph.get_state_history(config)]
# print(len(all_states))

to_fork = all_states[-2]
print(to_fork.values["messages"])
print(to_fork.config)
fork_config=graph.update_state(to_fork.config,
                               {"messages" : [HumanMessage(content="Multiply 5 and 6",
                                                          id=to_fork.values["messages"][0].id)]}
                               )
print(fork_config)
all_states = [state for state in graph.get_state_history(fork_config)]
print(all_states[0].values["messages"])

for event in graph.stream(None,fork_config,stream_mode="values"):
    event["messages"][-1].pretty_print()

all_states = [state for state in graph.get_state_history(config)]
print(len(all_states))