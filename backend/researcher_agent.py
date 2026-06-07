from typing import TypedDict
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START,END

class ResearchState(TypedDict):
    query:str
    research:str

llm=ChatOllama(
    model="qwen3:8b",
    temperature=0
)

def research_agent(state: ResearchState):
    prompt=f"""
    You are an expert researcher.
    Research the following topic and provide detailed factual information.
    Topic:
    {state["query"]}
    """
    response=llm.invoke(prompt)
    return{
        "query":state["query"],
        "research":response.content
    }

graph_builder=StateGraph(ResearchState)
graph_builder.add_node(
    "researcher",
    research_agent
)
graph_builder.add_edge(
    START,
    "researcher"
)
graph_builder.add_edge(
    "researcher",
    END
)
graph=graph_builder.compile()
test_state={
    "query":"What is LangGraph",
    "research":""
}
result=graph.invoke(test_state)
print(result)
