from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    # The methods should return True if the request should be granted access, and False otherwise.
    # has_object_permission is object-level permission only ! not global permission !
    # for global permission use has_permission instead
    def has_object_permission(self, request, view, obj):
        # Check permissions for read-only request
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check permissions for write request
        else:
            # Write permissions are only allowed to the owner of the snippet.
            return obj.user == request.user