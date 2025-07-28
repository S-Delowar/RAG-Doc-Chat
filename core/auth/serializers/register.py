from rest_framework import serializers

from core.user.models import CustomUser
from core.user.serializers import CustomUserSerializer

from django.contrib.auth import get_user_model

User = get_user_model()



class RegisterSerializer(CustomUserSerializer):
    """
    Registration serializer for request for user creation
    """
    
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_active',
            'is_staff',
            'date_joined',
        ]
        read_only_fields = ['id', 'is_active', 'is_staff', 'date_joined']

        def create(self, validated_data):
            password = validated_data.pop('password')
            user = User.objects.create_user(password=password, **validated_data)
            return user