import chromadb
import uuid

client=chromadb.PersistentClient(
    path="./chroma_db"
)

collection=client.get_or_create_collection(
    name="HiveMemory"
)

THRESHOLD=1.2

def save_memory(query,answer):
    document=f"""
    Questions:
    {query}
    Answer:
    {answer}
    """

    collection.add(
        ids=[str(uuid.uuid4())],
        documents=[document]
    )

def search_memory(query):
    result=collection.query(
        query_texts=[query],
        n_results=1
    )
    if not result["documents"][0]:
        return None
    document=result["documents"][0][0]
    distance=result["distances"][0][0]

    if distance>THRESHOLD:
        return None
    
    return{
        "document":document,
        "distance":distance
    }

result=search_memory("what did kratos do to baldur")
print(result)