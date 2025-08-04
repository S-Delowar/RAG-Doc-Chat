from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed

from core.chat.models.chat_message import ChatMessage
from core.chat.models.chat_session import ChatSession
from core.chat.models.document import Document
from core.chat.permissions import IsOwner
from core.chat.serializers.chat_message import ChatMessageSerializer
from core.chat.serializers.chat_session import ChatSessionSerializer
from core.chat.serializers.document import DocumentSerializer
from core.chat.tasks import run_memory_summarization


class ChatSessionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChatSessionSerializer
    queryset = ChatSession.objects.all()
    http_method_names = ['post', 'get', 'patch', 'delete']
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    
    @action(detail=True, methods=['post'], url_path="documents", permission_classes=[IsAuthenticated])
    def document_upload(self, request, pk=None):
        """ 
        Allow authenticated users to upload a document to their own session.
        """
        chat_session = self.get_object()
        
        serializer = DocumentSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save(session=chat_session)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    @action(detail=True, methods=['post'], url_path="messages", permission_classes=[IsAuthenticated])
    def get_message_response(self, request, pk=None):
        """ 
        Allow authenticated users to write message and get response from the AI agent.
        """
        chat_session = self.get_object()
        
        serializer = ChatMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(session=chat_session, sender="User")
        
        response = {
            'user': serializer.data["content"],
            'ai' : 'Hello Hoe can I help you?'
        }
        
        # Run summarization in background using Celery
        try:
            if ChatMessage.objects.filter(session=chat_session).count() > 10:
                run_memory_summarization.delay(chat_session.id)
        except:
            raise ValueError
        
        return Response(response, status=status.HTTP_201_CREATED)
    
     
class DocumentViewSet(viewsets.ModelViewSet):
    """
    Only allow update and delete of a single document.
    Listing and creation are disabled — documents are handled through ChatSession.
    """
    serializer_class = DocumentSerializer
    permission_classes = (IsOwner,)
    http_method_names = ['patch', 'delete']

    def get_queryset(self):
        return Document.objects.filter(session__user=self.request.user)

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")
    
    
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