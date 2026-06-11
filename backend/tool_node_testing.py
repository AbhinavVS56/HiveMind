from langchain.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage
from ddgs import DDGS

@tool
def calculator(expression: str)->str:
    """
    Evaluate a simple math expression
    """
    return str(eval(expression))

@tool
def weather(city: str) -> str:
    """
    Get current weather information for a city.
    """

    return f"The weather in {city} is sunny."

@tool
def web_search(query: str)->str:
    """
    Get the latest information on the query
    """
    with DDGS() as ddgs:
        result=list(ddgs.text(
            query,
            max_result=3
        ))
    return str(result)

llm=ChatOllama(
    model="qwen3:8b",
    temperature=0
)
llm_with_tools=llm.bind_tools([calculator, weather, web_search])

def chatbot(state: MessagesState):
    response=llm_with_tools.invoke(state["messages"])
    return{
        "messages":[response]
    }

tool_node=ToolNode([calculator,weather,web_search])

graph_builder=StateGraph(MessagesState)
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("tools",tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot",tools_condition)
graph_builder.add_edge("tools","chatbot")

graph=graph_builder.compile()

result=graph.invoke({
    "messages":[HumanMessage(content="What is latest AI news?")]
})

for message in result["messages"]:
    print()
    print(type(message))
    print(message)