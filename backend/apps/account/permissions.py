from rest_framework.permissions import BasePermission


class IsOwnerOrSuperuser(BasePermission):
    """
    Custom permission to allow users to access only their own data
    unless they are a superuser.
    """

    def has_object_permission(self, request, view, obj):
        # Superusers can access everything
        if request.user.is_superuser:
            return True

        # Regular users can only access their own data
        return obj.account_holder.user == request.user
