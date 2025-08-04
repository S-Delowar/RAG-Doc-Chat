from rest_framework import serializers

from core.chat.models.chat_message import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'content', 'timestamp']
        read_only_fields = ['id', 'sender', 'timestamp']