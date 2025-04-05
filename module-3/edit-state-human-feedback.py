import dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, StateGraph,START,END
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from pprint import pprint
dotenv.load_dotenv()

def multiply(a:int,b:int):
    """
    multiply two integer
    Args:
        a: first integer
        b: second integer
    """
    return a * b

def add(a:int,b:int):
    """
    add two integers
    Args:
        a: first integer
        b: second integer
    """
    return a + b

def subtract(a:int,b:int):
    """
    subtract two integers
    Args:
        a: first integer
        b: second integer
    """
    return a - b

tools=[multiply, add, subtract]
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools=llm.bind_tools(tools)

# Node
def assistant(state):
    return {"messages" : [llm_with_tools.invoke(state["messages"])]}

def human_feedback(state):
    pass

builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools",ToolNode(tools))
builder.add_node("human_feedback",human_feedback)

builder.add_edge(START,"human_feedback")
builder.add_edge("human_feedback","assistant")
builder.add_conditional_edges("assistant",tools_condition)
builder.add_edge("tools","assistant")

memory = MemorySaver()
graph = builder.compile(interrupt_before=["human_feedback"] , checkpointer=memory)

config = {"configurable" :{"thread_id" : "1"}}

input_message=[HumanMessage(content="Multiply 2 and 5")]
for event in graph.stream({"messages":input_message},config, stream_mode="values"):
    event["messages"][-1].pretty_print()

# state = graph.get_state(config)
# # print(f"Graph interrupted, Next Node will be : {state.next}")

# user_approval = input("Do you want to call the tool? (yes/no): ")

# if user_approval.lower() == 'yes':
#     for event in graph.stream(None, config, stream_mode="values"):
#         event['messages'][-1].pretty_print()
# else:
#     print("Operations aborted")

# state = graph.get_state(config)
# print(state)

# graph.update_state(config,{"messages" : HumanMessage(content="Instead, Multiply 3 and 6")})

# state = graph.get_state(config)
# print(state)

# for event in graph.stream(None,config, stream_mode="values"):
#     event["messages"][-1].pretty_print()

user_input = input("How do you want to update state?")
graph.update_state(config,{"messages" : user_input}, as_node="human_feedback")

for event in graph.stream(None,config,stream_mode="values"):
    event["messages"][-1].pretty_print()