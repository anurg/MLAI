# load OPENAI_API_KEY

import dotenv
dotenv.load_dotenv()

# define multiply function
def multiply(a: int, b: int) -> int:
    """
    Multiply a and b
    Args:
        a: first int
        b: second int
    """
    return a * b

# define llm
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")

# define llm with tools
llm_with_tools = llm.bind_tools([multiply])

# build the graph
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
# import MessagesState
from langgraph.graph.message import MessagesState
# import toolnode, tools_condition
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

# Define Node
def tool_calling_llm(state:MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build Graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([multiply]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm", tools_condition)
builder.add_edge("tools",END)
graph = builder.compile()

# display(Image(graph.get_graph().draw_mermaid_png()))

from langchain_core.messages import HumanMessage
# messages = graph.invoke({ "messages": HumanMessage(content="Hello", name="Lance") })
messages = graph.invoke({ "messages": HumanMessage(content="multiply 20 with 4", name="Lance") })

for m in messages["messages"]:
    m.pretty_print()





