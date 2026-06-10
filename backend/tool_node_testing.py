from langchain.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage

@tool
def calculator(expression: str)->str:
    """
    Evaluate a simple math expression
    """
    return str(eval(expression))

llm=ChatOllama(
    model="qwen3:8b",
    temperature=0
)
llm_with_tools=llm.bind_tools([calculator])

def chatbot(state: MessagesState):
    response=llm_with_tools.invoke(state["messages"])
    return{
        "messages":[response]
    }

tool_node=ToolNode([calculator])

graph_builder=StateGraph(MessagesState)
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("tools",tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot",tools_condition)
graph_builder.add_edge("tools","chatbot")

graph=graph_builder.compile()

result=graph.invoke({
    "messages":[HumanMessage(content="What is 69*69")]
})

for message in result["messages"]:
    print()
    print(type(message))
    print(message)