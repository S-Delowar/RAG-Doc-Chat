from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from core.user.serializers import CustomUserSerializer


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'put'], url_path='me')
    def me(self, request):
        if request.method == 'GET':
            serializer = CustomUserSerializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
