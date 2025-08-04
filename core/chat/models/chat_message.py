from django.db import models
import uuid

from core.chat.models.chat_session import ChatSession


class ChatMessage(models.Model):
    """ Represents a single message in a chat session """
    SENDER_CHOICES = [
        ('user', 'User'), 
        ('bot', 'Bot')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
        
    def __str__(self):
        return f"[{self.sender}] {self.content[:50]}"