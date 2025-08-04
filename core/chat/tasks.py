from celery import shared_task
from core.chat.models import ChatSession
from core.chat.rag.memory.summarize_old_messages import summarize_old_messages


@shared_task
def run_memory_summarization(session_id):
    try:
        print(f"Memory function trigered.......!")
        session = ChatSession.objects.get(id=session_id)
        summarize_old_messages(session)
    except ChatSession.DoesNotExist:
        pass
        