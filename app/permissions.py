from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,

        # Check permissions for read-only request, or
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check permissions for write request , or
        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user
    

# class IsStaffOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to only allow owners of an object to edit it.
#     """

#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,

#         # Check permissions for read-only request, or
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # Check permissions for write request , or
#         # Write permissions are only allowed to the owner of the snippet.
#         return obj.user == request.user
    