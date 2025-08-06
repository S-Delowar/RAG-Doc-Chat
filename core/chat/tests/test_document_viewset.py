import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
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
def document(chat_session):
    return Document.objects.create(file="test_file.pdf", session=chat_session)


# -------------------------
# Tests
# -------------------------
dummy_file = SimpleUploadedFile("file.txt", b"Dummy content", content_type="text/plain")

@pytest.mark.django_db
def test_patch_document(auth_client, document):
    url = f"/api/documents/{document.id}/"
    data = {
        "file": dummy_file,
    }
    response = auth_client.patch(url, data, format="multipart")
    assert response.status_code == status.HTTP_200_OK
    updated_doc = Document.objects.get(id=document.id)
    assert updated_doc.file.name.endswith("file.txt")

@pytest.mark.django_db
def test_delete_document(auth_client, document):
    url = f"/api/documents/{document.id}/"
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
@pytest.mark.django_db
def test_list_document_not_allowed(auth_client):
    url = "/api/documents/"
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
@pytest.mark.django_db
def test_create_document_method_not_allowed(auth_client):
    url = "/api/documents/"
    data = {
        "file": dummy_file,
    }
    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    