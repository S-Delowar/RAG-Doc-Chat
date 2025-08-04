from rest_framework import serializers

from core.chat.models.chat_session import ChatSession
from core.chat.serializers.chat_message import ChatMessageSerializer
from core.chat.serializers.document import DocumentSerializer

class ChatSessionSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    chat_messages = ChatMessageSerializer(many=True, read_only=True)
    

    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'title', 'created_at', 'documents', 'chat_messages'] 
        read_only_fields = ('id', 'user', 'created_at')   