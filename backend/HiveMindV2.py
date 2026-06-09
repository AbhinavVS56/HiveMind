from typing import TypedDict
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START,END
#import time

class ResearchState(TypedDict):
    query:str
    research:str
    analysis:str
    critique:str
    final_answer:str
    need_critic:bool

llm=ChatOllama(
    model="qwen3:8b",
    temperature=0
)

def research_agent(state: ResearchState):
    #start=time.time()
    prompt=f"""
    You are an expert researcher.
    Research the following topic.
    Provide:
    - Maximum 3 bullet points
    - Maximum 80 words total
    - Only factual information
    Topic:
    {state["query"]}
    """
    response=llm.invoke(prompt)
    #print(f"Researcher took {time.time()-start:.2f} seconds")
    return{
        "research":response.content
    }

def analysis_agent(state: ResearchState):
    #start=time.time()
    prompt=f"""
    You are an expert analyst.
    Analyze the research below and provide exactly 2 key insights.
    Maximum 80 words.
    Research:
    {state['research']}
    """
    response=llm.invoke(prompt)
    #print(f"Analyst took {time.time()-start:.2f} seconds")
    return{
        "analysis":response.content
    }

def decision_agent(state: ResearchState):
    #start=time.time()
    prompt=f"""
    You are a workflow manager.
    A critique step is required when:
    -The query asks for comparisions
    -The query involves opinions
    -The query involves trade-offs
    -The query involves recommendations
    -The query involves controversial topics

    A critique step is NOT needed when:
    -The query asks for simple facts
    -The query asks for definitions
    -The query asks for straightforward explanations

    Return only YES or NO
    Query:
    {state['query']}
    """
    response=llm.invoke(prompt)
    answer=response.content.upper()
    #print("RAW RESPONSE:")
    #print(response.content)
    #print(f"Decision Agent took {time.time()-start:.2f} seconds")
    return{
        "need_critic": "YES" in answer
    }

def route_decision(state: ResearchState):
    if state["need_critic"]:
        return "critic"
    return "writer"

def critic_agent(state: ResearchState):
    #start=time.time()
    prompt=f"""
    You are an expert critic.
    Review the research and analysis below.
    Identify:
    -Weakness
    -Missing information
    -Possible inaccuracies
    -Alternative viewpoints
    Provide at most 2 criticisms.
    Maximum 80 words.
    Research:
    {state['research']}
    Analysis:
    {state['analysis']}
    """
    response=llm.invoke(prompt)
    #print(f"Critic took {time.time()-start:.2f} seconds")
    return{
        "critique":response.content
    }

def writer_agent(state: ResearchState):
    #start=time.time()
    prompt=f"""
    You are an expert technical writer.
    Using the research, analysis and critique below,
    create a clear, balanced and well structured final answer.
    Maximum 150 words.
    Research:
    {state['research']}
    Analysis:
    {state['analysis']}
    Critique:
    {state['critique']}
    """
    response=llm.invoke(prompt)
    #print(f"Writer took {time.time()-start:.2f} seconds")
    return{
        "final_answer":response.content
    }

graph_builder=StateGraph(ResearchState)

graph_builder.add_node("researcher",research_agent)
graph_builder.add_node("analyst",analysis_agent)
graph_builder.add_node("critic",critic_agent)
graph_builder.add_node("writer",writer_agent)
graph_builder.add_node("decision",decision_agent)

graph_builder.add_edge(START,"researcher")
graph_builder.add_edge("researcher","analyst")
graph_builder.add_edge("analyst","decision")
graph_builder.add_conditional_edges("decision",
                                    route_decision,
                                    {
                                        "critic":"critic",
                                        "writer":"writer"
                                    }
                                )
graph_builder.add_edge("critic","writer")
graph_builder.add_edge("writer",END)

graph=graph_builder.compile()
#print(graph.get_graph().draw_mermaid())

test_state={
    "query":"Compare LangGraph and CrewAI",
    "research":"",
    "analysis":"",
    "need_critic":"",
    "critique":"",
    "final_answer":""
}

result=graph.invoke(test_state)
print(result["final_answer"])