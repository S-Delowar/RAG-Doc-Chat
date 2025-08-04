import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.user.models import CustomUser


# -------------------------
# Fixtures
# -------------------------

@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='testpass123',
        first_name='first',
        last_name='last',
    )

@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


# -------------------------
# UserViewSet Tests
# -------------------------

@pytest.mark.django_db
def test_get_authenticated_user_profile(auth_client, user):
    response = auth_client.get("/api/user/me/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == user.email
    assert response.data['username'] == user.username

    
@pytest.mark.django_db
def test_patch_authenticated_user_profile_valid(auth_client, user):
    payload = {
        'first_name': 'first_updated',
        'last_name': 'last_updated'
    }
    response = auth_client.patch("/api/user/me/", data=payload)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.first_name == "first_updated"
    assert user.last_name == "last_updated"
    
    
@pytest.mark.parametrize('field', ['email', 'username'])
def test_patch_disallowed_fields(auth_client, field):
    data = {
        field: "edited@example.com" if field == 'email' else 'edited-username'
    }
    response = auth_client.patch('/api/user/me/', data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert field in response.data
    assert f"You cannot update your {field}." in response.data[field]


@pytest.mark.django_db
def test_unauthenticated_user_not_get_user_profile():
    client = APIClient()
    response = client.get("/api/user/me/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
