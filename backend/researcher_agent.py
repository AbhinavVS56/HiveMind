from typing import TypedDict
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START,END

class ResearchState(TypedDict):
    query:str
    research:str
    analysis:str
    critique:str
    final_answer:str

llm=ChatOllama(
    model="qwen3:8b",
    temperature=0
)

def research_agent(state: ResearchState):
    prompt=f"""
    You are an expert researcher.
    Research the following topic and provide concise factual information.
    Maximum 5 bullet points.
    Topic:
    {state["query"]}
    """
    response=llm.invoke(prompt)
    return{
        "research":response.content
    }

def analysis_agent(state: ResearchState):
    prompt=f"""
    You are an expert analyst.
    Analyze the research below and provide 3 key insights only.
    Maximum 150 words.
    Research:
    {state['research']}
    """
    response=llm.invoke(prompt)
    return{
        "analysis":response.content
    }

def critic_agent(state: ResearchState):
    prompt=f"""
    You are an expert critic.
    Review the research and analysis below.
    Identify:
    -Weakness
    -Missing information
    -Possible inaccuracies
    -Alternative viewpoints
    Provide at most 3 criticisms.
    Maximum 150 words.
    Research:
    {state['research']}
    Analysis:
    {state['analysis']}
    """
    response=llm.invoke(prompt)
    return{
        "critique":response.content
    }

def writer_agent(state: ResearchState):
    prompt=f"""
    You are an expert technical writer.
    Using the research, analysis and crtique below,
    create a clear, balanced and well structured final answer.
    Maximum 300 words.
    Research:
    {state['research']}
    Analysis:
    {state['analysis']}
    Critique:
    {state['critique']}
    """
    response=llm.invoke(prompt)
    return{
        "final_answer":response.content
    }

graph_builder=StateGraph(ResearchState)

graph_builder.add_node("researcher",research_agent)
graph_builder.add_node("analyst",analysis_agent)
graph_builder.add_node("critic",critic_agent)
graph_builder.add_node("writer",writer_agent)

graph_builder.add_edge(START,"researcher")
graph_builder.add_edge("researcher","analyst")
graph_builder.add_edge("analyst","critic")
graph_builder.add_edge("critic","writer")
graph_builder.add_edge("writer",END)

graph=graph_builder.compile()

test_state={
    "query":"What is LangGraph",
    "research":"",
    "analysis":"",
    "critique":"",
    "final_answer":""
}

result=graph.invoke(test_state)
print(result)