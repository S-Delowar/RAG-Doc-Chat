from django.contrib import admin

from core.chat.models.chat_message import ChatMessage
from core.chat.models.chat_session import ChatSession
from core.chat.models.chat_summary import ChatMemory
from core.chat.models.document import Document


# Registering the models
admin.site.register(ChatSession)
admin.site.register(ChatMessage)
admin.site.register(Document)
admin.site.register(ChatMemory)