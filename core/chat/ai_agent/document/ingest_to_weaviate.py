import weaviate
from core.chat.ai_agent.document.loader import load_document
from core.chat.ai_agent.document.splitter import split_documents
from core.chat.ai_agent.vectorstore.weaviate import get_weaviate_client


def ingest_to_weaviate(session_id: str, file_path: str):
    """
    Loads a file, splits into chunks, and ingests into Weaviate.
    Each chunk gets stored with a session_id so it’s private to that user session.
    """
    client = get_weaviate_client()
    collection = client.collections.get("Document")

    # Load and Split
    docs = load_document(file_path)
    chunks = split_documents(docs)

    # Prepare data
    data_objs = [
        {
            "session_id": session_id,
            "content": chunk.page_content,
            "source": file_path
        }
        for chunk in chunks
    ]

    collection.data.insert_many(data_objs)
    print(f"Ingested {len(data_objs)} chunks for session {session_id}")

    client.close()