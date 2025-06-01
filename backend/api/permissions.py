from rest_framework import permissions, status
from core.settings import base as settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated

class IsCompanySuperuser(permissions.BasePermission):
    message = "Вы должны быть суперпользователем компании, чтобы выполнить это действие"
    
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_company_superuser
        )

class IsAuthed(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            raise NotAuthenticated(
                detail="Authentication credentials were not provided.",
                code=status.HTTP_401_UNAUTHORIZED
            )
        return True

class IsAuthedOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not super().has_permission(request, view):
            raise NotAuthenticated(
                detail="Authentication credentials were not provided.",
                code=status.HTTP_401_UNAUTHORIZED
            )
        return True

class IsDebug(permissions.BasePermission):
    def has_permission(self, request, view):
        return settings.DEBUG