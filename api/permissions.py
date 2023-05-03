from rest_framework.permissions import IsAuthenticatedOrReadOnly


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsAuthenticatedStaffOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.is_staff
        )