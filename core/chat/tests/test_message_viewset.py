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

@pytest.fixture
def message(chat_session):
    return ChatMessage.objects.create(session=chat_session, sender="User", content="Hi")

# -------------------------
# Tests
# -------------------------
@pytest.mark.django_db
def test_patch_message(auth_client, message):
    url = f"/api/messages/{message.id}/"
    response = auth_client.patch(url, {"content": "Updated"})
    assert response.status_code == status.HTTP_200_OK
    assert ChatMessage.objects.get(id=message.id).content == "Updated"

@pytest.mark.django_db
def test_delete_message(auth_client, message):
    url = f"/api/messages/{message.id}/"
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_list_message_method_not_allowed(auth_client):
    url = f"/api/messages/"
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

@pytest.mark.django_db
def test_create_message_method_not_allowed(auth_client):
    url = f"/api/messages/"
    response = auth_client.post(url, {"content": "Hello"})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED