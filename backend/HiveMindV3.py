from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START,END
from langchain.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from ddgs import DDGS
from langgraph.prebuilt import ToolNode, tools_condition
from memory import search_memory
import time

class ResearchState(TypedDict):
    messages:Annotated[list,add_messages]
    query:str
    research:str
    analysis:str
    critique:str
    final_answer:str
    need_critic:bool
    memory:str
    memory_distance:float

llm=ChatOllama(
    model="qwen3:8b",
    temperature=0
)

@tool
def web_search(query:str)->str:
    """
    Search the web for the current information
    """
    with DDGS() as ddgs:
        results=list(ddgs.text(
            query,
            max_result=1
        ))
    return str(results)

llm_tools=llm.bind_tools(
    [
        web_search
    ]
)

tool_node=ToolNode(
    [
        web_search
    ]
)

def memory_agent(state: ResearchState):
    result=search_memory(state["query"])
    if result is None:
        print("No memory found")
        return {}
    print("Memory found")
    return{
        "memory":result["document"],
        "memory_distance":result["distance"]
    }

def RAG_agent(state: ResearchState):
    messages=[
        SystemMessage(
            content="""
            You are a helpful assistant.
            Use the retrieved memory to answer the user's question.
            If the memory is relevant, use it as context for your answer.
            """
        ),
        HumanMessage(
            content=f"""
            Relevant Message:{state['memory']}
            User Question:{state['query']}
            """
        )
    ]
    response=llm.invoke(messages)
    return{
        "final_answer":response.content
    }

def research_agent(state: ResearchState):
    if not state["messages"]:
        messages = [
            SystemMessage(
                content="""
                You are an expert researcher.
                Research the user's topic.
                Use web search whenever:
                - The answer depends on factual accuracy
                - The answer refers to a specific person, game, event, company, technology, or topic
                - You are uncertain
                - Additional context could improve accuracy
                When in doubt, search first.
                Provide:
                - Maximum 3 bullet points
                - Maximum 80 words total
                - Only factual information
                """
            ),
            HumanMessage(
                content=state["query"]
            )
        ]
    else:
        messages = state["messages"]
    start=time.time()
    response = llm_tools.invoke(messages)
    print(f"Researcher took {time.time()-start:.2f} seconds")
    print("TOOL CALL", response.tool_calls)
    if response.tool_calls:
        return {
            "messages": [response]
        }
    return {
        "messages": [response],
        "research": response.content
    }

def analysis_agent(state: ResearchState):
    start=time.time()
    prompt=f"""
    You are an expert analyst.
    Analyze the research below and provide exactly 2 key insights.
    Maximum 80 words.
    Research:
    {state['research']}
    """
    response=llm.invoke(prompt)
    print(f"Analyst took {time.time()-start:.2f} seconds")
    return{
        "analysis":response.content
    }

def decision_agent(state: ResearchState):
    start=time.time()
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

    Return only YES or NO and it should be quick.
    Most favourable will be few seconds cause it's just a yes/no answer.
    Query:
    {state['query']}
    """
    response=llm.invoke(prompt)
    answer=response.content.upper()
    #print("RAW RESPONSE:")
    #print(response.content)
    print(f"Decision Agent took {time.time()-start:.2f} seconds")
    return{
        "need_critic": "YES" in answer
    }

def route_decision(state: ResearchState):
    if state["need_critic"]:
        return "critic"
    return "writer"

def memory_router(state):
    if state["memory"]:
        return "RAG"
    return "researcher"

def critic_agent(state: ResearchState):
    start=time.time()
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
    print(f"Critic took {time.time()-start:.2f} seconds")
    return{
        "critique":response.content
    }

def writer_agent(state: ResearchState):
    start=time.time()
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
    print(f"Writer took {time.time()-start:.2f} seconds")
    return{
        "final_answer":response.content
    }

graph_builder=StateGraph(ResearchState)

graph_builder.add_node("memory",memory_agent)
graph_builder.add_node("RAG",RAG_agent)
graph_builder.add_node("researcher",research_agent)
graph_builder.add_node("tools",tool_node)
graph_builder.add_node("analyst",analysis_agent)
graph_builder.add_node("critic",critic_agent)
graph_builder.add_node("writer",writer_agent)
graph_builder.add_node("decision",decision_agent)

graph_builder.add_edge(START,"memory")
graph_builder.add_conditional_edges("memory",memory_router,{
                                "RAG":"RAG",
                                "researcher":"researcher"    
                            }
                        )
graph_builder.add_edge("RAG",END)
graph_builder.add_conditional_edges("researcher",tools_condition,{
                                "tools":"tools",
                                END:"analyst"
                            }
                        )
graph_builder.add_edge("tools","researcher")
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
    "messages":[],
    "query":"What did Kratos do to Baldur?",
    "research":"",
    "analysis":"",
    "need_critic":False,
    "critique":"",
    "final_answer":"",
    "memory":"",
    "memory_distance":0.0
}

#print(web_search.invoke(
#    {"query":"Which mainline resident evil games features Leon in it"}
#))

result=graph.invoke(test_state)
print(result["final_answer"])