from langchain.chat_models import init_chat_model
from core.chat.ai_agent.constants import OPENAI_MODEL_NAME
import os
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    llm = init_chat_model(
        OPENAI_MODEL_NAME, 
        model_provider="openai",
        api_key=os.getenv("OPENAI_API_KEY")
        )
    return llm

