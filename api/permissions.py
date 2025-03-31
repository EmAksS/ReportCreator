from rest_framework import permissions

class IsCompanySuperuser(permissions.BasePermission):
    message = "Вы должны быть суперпользователем компании, чтобы выполнить это действие"
    
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_superuser_of_company
        )