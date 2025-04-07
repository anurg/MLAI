from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.tools import TavilySearchResults
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph,START,END
from IPython.display import Image, display

class State(TypedDict):
    question:str
    answer: str
    context:Annotated[list,add]

llm=ChatOpenAI(model="gpt-4o",temperature=0)

def search_web(state):
    """Retrieves docs from web search"""
    tavily_search = TavilySearchResults(max_results=3)
    search_docs = tavily_search.invoke(state["question"])

    formatted_search_docs = "\n\n--\n\n".join(
        [
            f'<Document href="{doc["url"]}">\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
        
    )
    return {"context":[formatted_search_docs]}

def search_wikipedia(state):
    """Retrieves docs from wikipedia"""
    search_docs = WikipediaLoader(query=state["question"], load_max_docs=2).load()
    formatted_search_docs = "\n\n -- \n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}">\n {doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )
    return {"context" : [formatted_search_docs]}
def generate_answer(state):
    """ Node to generate an answer"""
    context=state["context"]
    question=state["question"]
    answer_template=f"Answer this question {question} using the context {context}"
    answer_instructions = answer_template.format(question,context)

    result = llm.invoke([SystemMessage(content=answer_instructions)] + [HumanMessage(content="Answer the question")])
    return {"answer":result}

builder = StateGraph(State)
builder.add_node("search_web",search_web)
builder.add_node("search_wiki",search_wikipedia)
builder.add_node("generate_answer",generate_answer)

builder.add_edge(START,"search_web")
builder.add_edge(START,"search_wiki")
builder.add_edge("search_web","generate_answer")
builder.add_edge("search_wiki","generate_answer")
builder.add_edge("generate_answer",END)

graph = builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))

result = graph.invoke({"question":"When was the latest earthquake in Asia which cuased serious damages?"})
print(result["answer"].content)