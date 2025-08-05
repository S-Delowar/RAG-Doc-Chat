from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed

from core.chat.models.document import Document
from core.chat.serializers.document import DocumentSerializer
from core.chat.permissions import IsOwner


class DocumentViewSet(viewsets.ModelViewSet):
    """
    Only allow update and delete of a single document.
    Listing and creation are disabled — documents are handled through ChatSession.
    """
    serializer_class = DocumentSerializer
    permission_classes = (IsOwner,)
    http_method_names = ['patch', 'delete']

    def get_queryset(self):
        return Document.objects.filter(session__user=self.request.user)

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")
    