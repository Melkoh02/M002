from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated

from users.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_admin or user.is_superuser))


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsDirector(IsAuthenticated):

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        if not request.user.user_type == User.UserType.DIRECTOR:
            return False

        return True


class IsSecretary(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        if not request.user.user_type == User.UserType.SECRETARY:
            return False

        return True


class IsProfessor(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        if not request.user.user_type == User.UserType.PROFESSOR:
            return False

        return True
