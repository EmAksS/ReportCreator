from django.urls import path
from .views import (
    users,
    company
)

urlpatterns = [
    path('csrf/', users.get_csrf_token, name='csrf_token'),
    path('check_auth/', users.check_auth, name='check_auth'),
    path('login/', users.login_view, name='login'),
    path('logout/', users.logout_view, name='logout'),
    path('register/company/', company.register_company, name='register_company'),
    path('register/user/', users.register_user, name='register_user'),
    path('company/', company.get_company_info, name='get_company_info'),
]
