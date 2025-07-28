from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Session(models.Model):
    """ A chat session created by the user. """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title or f"Session {self.id}"