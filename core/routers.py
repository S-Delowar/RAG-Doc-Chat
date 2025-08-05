from rest_framework import routers

from core.auth.viewsets.login import LoginViewSet
from core.auth.viewsets.refresh import RefreshViewSet
from core.auth.viewsets.register import RegisterViewSet
from core.chat.viewsets.chat_message import ChatMessageViewSet
from core.chat.viewsets.chat_session import ChatSessionViewSet
from core.chat.viewsets.document import DocumentViewSet
from core.user.viewsets import UserViewSet

router = routers.SimpleRouter()

# User
router.register(r'user', UserViewSet, basename='user')

# AUTH
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename='auth-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

# Session 
router.register(r'sessions', ChatSessionViewSet, basename="chat-session")

# Document update and delete
router.register(r'documents', DocumentViewSet, basename='session-document')

# Message update and delete
router.register(r'messages', ChatMessageViewSet, basename='chat-message')


urlpatterns = [
    *router.urls,
]