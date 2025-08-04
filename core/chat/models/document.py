import os
from django.db import models
import uuid

from core.chat.models.chat_session import ChatSession


def user_session_document_path(instance, filename):
    # instance is Document model instance
    username = instance.session.user.username
    session_id = str(instance.session.id)
    return os.path.join('documents', username, session_id, filename)


class Document(models.Model):
    """ Documents uploaded by the user for a particular session """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to=user_session_document_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file.name