import os
from core.chat.ai_agent.utils.llm_utils import get_llm
from core.chat.models import ChatMemory, ChatMessage
from langchain_core.prompts import PromptTemplate


SUMMARY_PROMPT = PromptTemplate.from_template("""
            Summarize the following conversation history. Retain key facts, names, and questions/answers.
            
            {chat_history}                                      
        """)

def summarize_old_messages(session):
    messages = (ChatMessage.objects.filter(session=session).order_by('timestamp'))
    
    total = messages.count()
    
    if total <= 10:
        # Not enough history yet
        return 
    
    old_messages = messages[:total-10]
    formatted = "\n".join([f"{m.sender}: {m.content}" for m in old_messages])
    
    llm = get_llm()
    chain = SUMMARY_PROMPT | llm
    result = chain.invoke(({"chat_history": formatted}))
    summary = result.content.strip()
    
    ChatMemory.objects.update_or_create(
        session = session,
        defaults={"long_term_summary": summary}
    )