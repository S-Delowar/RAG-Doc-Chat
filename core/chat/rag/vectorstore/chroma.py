from langchain_chroma import Chroma
from core.chat.rag.constants import CHROMA_PERSIST_DIR
from core.chat.rag.embeddings.embedder import get_embedder

def get_chroma_vectorstore(collection_name: str):
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embedder(),
        persist_directory=CHROMA_PERSIST_DIR
    )


