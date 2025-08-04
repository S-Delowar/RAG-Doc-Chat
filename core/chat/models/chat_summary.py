from django.db import models
from core.chat.models.chat_session import ChatSession

class ChatMemory(models.Model):
    session = models.OneToOneField(ChatSession, on_delete=models.CASCADE, related_name="memory")
    long_term_summary = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Memory for Session {self.session.id}"