import chromadb
from langchain_ollama import ChatOllama

client=chromadb.PersistentClient(
    path="./chroma_db"
)

collection=client.get_or_create_collection(
    name="HiveMemory"
)

llm=ChatOllama(
    model="qwen3:8b",
    temperature=0
)

question="Why do fans dislike RE5"

result=collection.query(
    query_texts=[question],
    n_results=1
)

prompt=f"""
You are a helpful assistant.
Relevant Memory:
{result["documents"][0][0]}
Use the memory if it is relevant or needed.
If the memory is insufficient, answer using your own knowledge
User Question:
{question}
Answer:
"""

response=llm.invoke(prompt)

print(response.content)