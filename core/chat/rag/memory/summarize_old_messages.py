import os
from core.chat.models import ChatMemory, ChatMessage
from  langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
load_dotenv()


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
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo", 
        temperature=0.2,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    
    chain = SUMMARY_PROMPT | llm
    result = chain.invoke(({"chat_history": formatted}))
    summary = result.content.strip()
    
    ChatMemory.objects.update_or_create(
        session = session,
        defaults={"long_term_summary": summary}
    )