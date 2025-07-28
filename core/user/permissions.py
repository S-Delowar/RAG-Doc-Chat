from rest_framework import permissions

class IsSelfOrSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow if the user is superuser
        if request.user.is_superuser:
            return True
        # Allow if the user is accessing their own user object
        return obj == request.user