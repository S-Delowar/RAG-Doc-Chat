from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from core.chat.ai_agent.agent_runner import run_agent
from core.chat.models.chat_message import ChatMessage
from core.chat.models.chat_session import ChatSession
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

        # Save user message
        serializer = ChatMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(session=chat_session, sender="User")

        user_query = request.data["content"]

        # Run LLM agent
        ai_response = run_agent(session=chat_session, user_query=user_query)

        # Save AI response
        ChatMessage.objects.create(session=chat_session, content=ai_response, sender="AI")

        # Periodic memory summarization (every 10 messages)
        try:
            if ChatMessage.objects.filter(session=chat_session).count() % 10 == 0:
                run_memory_summarization.delay(chat_session.id)
        except Exception as e:
            print(f"Error during memory summarization: {str(e)}")

        return Response({"ai_response": ai_response}, status=status.HTTP_201_CREATED)
    
