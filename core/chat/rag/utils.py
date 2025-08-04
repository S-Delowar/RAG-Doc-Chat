
from langchain.chat_models import init_chat_model
from langchain_huggingface import HuggingFaceEmbeddings


def get_llm():
    llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    return llm


def get_embedder():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return embeddings