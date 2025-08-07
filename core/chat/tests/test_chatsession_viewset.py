import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from core.chat.models.chat_message import ChatMessage
from core.chat.models.chat_session import ChatSession
from core.chat.models.document import Document


User = get_user_model()

# -------------------------
# Fixtures
# -------------------------
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username="test_user", email="test_user@mail.com", password="pass123")

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client
    
@pytest.fixture
def chat_session(user):
    return ChatSession.objects.create(title="Test Session", user=user)


# -------------------------
# Tests
# -------------------------
@pytest.mark.django_db
def test_create_chat_session(auth_client):
    response = auth_client.post("/api/sessions/", {"title": "New Session"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "New Session"
    
@pytest.mark.django_db
def test_list_chat_sessions(auth_client, chat_session):
    response = auth_client.get("/api/sessions/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

@pytest.mark.django_db
def test_upload_document(auth_client, chat_session):
    url = f"/api/sessions/{chat_session.id}/documents/"
    # Create a fake file in memory
    dummy_file = SimpleUploadedFile("file.txt", b"Dummy content", content_type="text/plain")
    data = {
        "file": dummy_file,
    }
    response = auth_client.post(url, data, format='multipart')
    assert response.status_code == status.HTTP_201_CREATED
    assert Document.objects.filter(session=chat_session).count() == 1

@pytest.mark.django_db
def test_get_message_response_success(auth_client, chat_session, monkeypatch):
    # Patch the AI function to return a dummy response instead of calling real LLM
    monkeypatch.setattr(
        "core.chat.viewsets.chat_session.run_agent",
        lambda *args, **kwargs: "AI Response"
    )
    url = f"/api/sessions/{chat_session.id}/messages/"
    data = {"content": "Hello!"}
    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "ai_response" in response.data
    assert ChatMessage.objects.filter(session=chat_session).count() == 2

@pytest.mark.django_db
def test_get_message_response_invalid(auth_client, chat_session):
    url = f"/api/sessions/{chat_session.id}/messages/"
    data = {"invalid_field": "Hello!"}
    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST