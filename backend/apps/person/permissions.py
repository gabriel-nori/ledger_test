from rest_framework.permissions import BasePermission
from apps.person.models import Person


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
        return obj.user == request.user

    def has_permission(self, request, view):
        blocked = Person.objects.filter(user=request.user)
        return not blocked
