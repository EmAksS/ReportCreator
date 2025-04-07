from rest_framework import permissions
from core.settings import base as settings

class IsCompanySuperuser(permissions.BasePermission):
    message = "Вы должны быть суперпользователем компании, чтобы выполнить это действие"
    
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_company_superuser
        )

class IsDebug(permissions.BasePermission):
    def has_permission(self, request, view):
        return settings.DEBUG