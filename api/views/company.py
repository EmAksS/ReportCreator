from rest_framework.decorators import api_view, permission_classes
# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
# Serializers
from api.serializers.user import UserSerializer
from api.serializers.company import CompanySerializer
# Response & auth
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
# models
from backend.models.company import Executor
from backend.models.user import User

# --- Регистрация компании и суперпользователя ---

@api_view(["POST"])
@permission_classes([AllowAny])
def register_company(request):
    company_name = request.data.get("company_name")
    company_fullName = request.data.get("company_fullName")
    username = request.data.get("username")
    password = request.data.get("password")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    patronymic = request.data.get("patronymic")
    
    if not all([company_name, username, password, first_name, last_name]):
        return Response(
            {"error": "Нужно заполнение всех полей"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Создаем компанию
    company = Executor.objects.create(
        company_name=company_name,
        company_fullName=company_fullName)
    
    # Создаем суперпользователя компании
    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            company=company,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            is_superuser_of_company=True,
            is_staff=True  # для доступа к админке если нужно
        )
    except Exception as e:
        company.delete()  # Откатываем создание компании при ошибке
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Автоматический логин после регистрации
    login(request, user)
    return Response({
        "status": "success",
        "company": CompanySerializer(company).data,
        "user": UserSerializer(user).data
    }, status=status.HTTP_201_CREATED)


# --- Получение информации о компании и пользователях ---

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_company_info(request):
    if not request.user.company:
        return Response(
            {"error": "У пользователя нет компании"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    company = request.user.company
    users = User.objects.filter(company=company)
    
    return Response({
        "company": CompanySerializer(company).data,
        "users": UserSerializer(users, many=True).data
    })