import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core.user.models import CustomUser


@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='test_password',
        first_name='first',
        last_name='last',
    )

@pytest.fixture
def auth_client(user):
    client = APIClient()
    return client



# Tests 
def test_login(auth_client, user):
    data = { "email": user.email, "password": "test_password" }
    response = auth_client.post("/api/auth/login/", data)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["access"]
    assert response.data["user"]["id"] == str(user.id)
    assert response.data["user"]["username"] == user.username
    assert response.data["user"]["email"] == user.email
    

@pytest.mark.django_db
def test_register(auth_client):
    data = {
        "username": "johndoe",
        "email": "johndoe@yopmail.com",
        "password": "test_password",
        "first_name": "John",
        "last_name": "Doe"
    }
    response = auth_client.post("/api/auth/register/", data)
    assert response.status_code == status.HTTP_201_CREATED
    
    
def test_refresh(auth_client, user):
    data = { "email": user.email, "password": "test_password" }
    response = auth_client.post("/api/auth/login/", data)
    assert response.status_code == status.HTTP_200_OK
    
    data_refresh = { "refresh": response.data['refresh'] } 
    response = auth_client.post("/api/auth/refresh/", data_refresh)
    response.status_code == status.HTTP_200_OK
    assert response.data["access"]