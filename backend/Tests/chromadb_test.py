import chromadb

client=chromadb.PersistentClient(
    path="./chroma_db"
)

collection=client.get_or_create_collection(
    name="HiveMemory"
)

collection.add(
    ids=["memory_1"],
    documents=[
        """
        Question:
        Why is Resident Evil 5 hated?

        Answer:
        Fans disliked the shift toward action gameplay,
        co-op focus, and reduced survival horror elements.
        """
    ]
)

result=collection.query(
    query_texts=["Why does fans dislike RE5"],
    n_results=1
)

print(result)