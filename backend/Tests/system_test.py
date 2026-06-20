from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm=ChatOllama(
    model="qwen3:8b",
    temperature=0
)
messages=[
    SystemMessage(
        content="You are a sarcastic assistant. Always answer sarcastically"
    ),
    HumanMessage(
        content="What is python" 
    )
]
response=llm.invoke(messages)
print(response.content)
