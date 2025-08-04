
from langchain_huggingface import HuggingFaceEmbeddings
from core.chat.rag.constants import EMBEDDING_MODEL_NAME


def get_embedder():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return embeddings