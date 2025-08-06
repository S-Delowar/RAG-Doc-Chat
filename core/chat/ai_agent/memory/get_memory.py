from core.chat.models import ChatMessage, ChatMemory


def get_memory_context(session):
    try:
        summary = session.memory.long_term_summary or ""
    except ChatMemory.DoesNotExist:
        summary = ""
        
    recent_msgs = (
            ChatMessage.objects.filter(session=session).order_by('-timestamp')[:10][::-1]
        )
    recent_history = "\n".join([f"{m.sender}: {m.content}" for m in recent_msgs])
    return f"Summary of previous chat history:\n{summary}\n\nRecent:\n{recent_history}"
        