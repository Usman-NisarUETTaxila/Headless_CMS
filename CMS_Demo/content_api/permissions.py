from rest_framework.permissions import BasePermission

class IsAuthenticatedOrAdminUser(BasePermission):
    def has_permission(self, request, view):
        # Allow access if using token authentication
        if request.user and request.user.is_authenticated:
            return True
        # Allow access if superuser/staff and using the Django admin session
        if request.user and request.user.is_staff:
            return True
        return False
