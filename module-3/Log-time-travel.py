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

current_state = graph.get_state(config)
# print(current_state)
all_states = [s for s in graph.get_state_history(config)]
# print(len(all_states))

#
# def print_states(graph, config):
#     """
#     Print LangGraph states in a readable, structured format
#     """
#     all_states = [s for s in graph.get_state_history(config)]
#     print(f"Total states: {len(all_states)}")
    
#     for i, state in enumerate(all_states):
#         print(f"\n{'='*50}")
#         print(f"STATE {i} - Step {state.metadata.get('step', 'N/A')}")
#         print(f"{'='*50}")
        
#         # Print what node is coming next
#         next_node = state.next[0] if state.next else "END"
#         print(f"Next node: {next_node}")
        
#         # Print what node wrote data in this step
#         source_node = None
#         if state.metadata.get('writes'):
#             source_node = list(state.metadata['writes'].keys())[0] if state.metadata['writes'] else None
#         print(f"Data written by: {source_node if source_node else 'None'}")
        
#         # Print messages in the state
#         if 'messages' in state.values:
#             messages = state.values['messages']
#             print(f"\nMessages ({len(messages)}):")
            
#             for j, msg in enumerate(messages):
#                 print(f"\n  Message {j+1}: {msg.type}")
                
#                 # Human message
#                 if msg.type == "human":
#                     print(f"  Content: {msg.content}")
                
#                 # AI message with tool calls
#                 elif msg.type == "ai" and msg.additional_kwargs.get('tool_calls'):
#                     tool_calls = msg.additional_kwargs['tool_calls']
#                     print(f"  Tool calls: {len(tool_calls)}")
#                     for call in tool_calls:
#                         print(f"    - Function: {call['function']['name']}")
#                         print(f"    - Arguments: {call['function']['arguments']}")
                
#                 # Regular AI message
#                 elif msg.type == "ai":
#                     print(f"  Content: {msg.content}")
                
#                 # Tool message
#                 elif msg.type == "tool":
#                     print(f"  Tool: {msg.name}")
#                     print(f"  Result: {msg.content}")

# # Call the function at the end of your code
# print_states(graph, config)
