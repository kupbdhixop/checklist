from rest_framework import permissions

class IsOwnerOrShared(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.has_perm(request.user)
