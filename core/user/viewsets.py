from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from core.user.serializers import CustomUserSerializer


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        methods=['PATCH'],
        description="Update current authenticated user's profile. `username` and `email` fields are not allowed to be updated."
    )

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request):
        if request.method == 'GET':
            serializer = CustomUserSerializer(request.user)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            restricted_fields = ['email', 'username']
            for field in restricted_fields:
                if field in request.data:
                    return Response(
                        {field: f"You cannot update your {field}."},
                        status=400
                    )

            serializer = CustomUserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
