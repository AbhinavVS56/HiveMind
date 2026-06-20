from langchain_ollama import ChatOllama

llm=ChatOllama(
    model="qwen3:8b",
    temperature=0
)

print("HiveMind started\nType exit to quit\n")
while True:
    inp=input("You: ")
    if inp.lower()=="exit":
        break
    response=llm.invoke(inp)
    print("\nHiveMind: ",response.content)
    print()