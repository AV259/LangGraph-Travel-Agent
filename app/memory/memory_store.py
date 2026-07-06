import chromadb

client = chromadb.PersistentClient(path="./data/chroma_db")

collection = client.get_or_create_collection(name="user_memory")

def save_memory(memory_text: str):

    collection.add(
        documents=[memory_text],
        ids=[memory_text]
    )

def retrieve_memory(query: str):

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    return results["documents"][0]
