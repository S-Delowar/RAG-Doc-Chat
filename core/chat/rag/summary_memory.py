from langchain.memory import ConversationSummaryBufferMemory
from langchain.llms import OpenAI

def get_summary_memory():
    return ConversationSummaryBufferMemory(
        llm=OpenAI(),
        return_messages=True,
        memory_key="chat_history"
    )
