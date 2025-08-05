from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from core.chat.models.chat_message import ChatMessage
from core.chat.serializers.chat_message import ChatMessageSerializer
from core.chat.permissions import IsOwner


class ChatMessageViewSet(viewsets.ModelViewSet):
    """
    Only allow update and delete of a user message.
    Listing and creation are disabled — messages are handled through ChatSession.
    """
    serializer_class = ChatMessageSerializer
    permission_classes = (IsOwner,)
    http_method_names = ['patch', 'delete']

    def get_queryset(self):
        return ChatMessage.objects.filter(session__user=self.request.user)

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")