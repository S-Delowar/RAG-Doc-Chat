from langchain_huggingface import HuggingFaceEmbeddings
from core.chat.ai_agent.constants import EMBEDDING_MODEL_NAME


def get_embedder():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    return embeddings