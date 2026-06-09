from langchain.tools import tool
from langchain_ollama import ChatOllama

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

llm_tools_inc=llm.bind_tools([calculator])
response=llm_tools_inc.invoke("What is 69*69")
print(response.tool_calls)

tool_call = response.tool_calls[0]

result = calculator.invoke(
    tool_call["args"]
)

print("Tool Result:", result)
final_response = llm.invoke(
    f"""
    The calculator returned:

    {result}

    Answer the user's question:
    What is 69 * 69?
    """
)

print(final_response.content)