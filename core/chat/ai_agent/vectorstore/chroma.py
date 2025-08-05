from langchain_chroma import Chroma
from core.chat.ai_agent.constants import CHROMA_PERSIST_DIR
from core.chat.ai_agent.utils.embedder_utils import get_embedder


def get_chroma_vectorstore(collection_name: str):
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embedder(),
        persist_directory=CHROMA_PERSIST_DIR
    )


