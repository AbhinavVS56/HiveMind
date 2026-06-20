from langchain_ollama import ChatOllama

llm=ChatOllama(model="qwen3:8b",temperature=1)
response=llm.invoke("Which is the most tallest mountain")
print(response.content)