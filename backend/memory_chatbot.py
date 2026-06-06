from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm=ChatOllama(
    model="qwen3:8b",
    temperature=0
)

messages=[
    SystemMessage(
      content="You are a very helpgul assistant"  
    )
]

print("HiveMind")
print("Type exit to quit\n")

while True:
    inp=input("You: ")
    if inp.lower()=="exit":
        break
    messages.append(
        HumanMessage(content=inp)
    )
    response=llm.invoke(messages)
    print("AI: \n",response.content)
    print()
    messages.append(
        AIMessage(content=response.content)
    )