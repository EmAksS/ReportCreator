from rest_framework.decorators import api_view, permission_classes
# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
# Serializers
from api.serializers.users import UserSerializer
from api.serializers.company import CompanySerializer, CompanyFieldSerializer
# Response & auth
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
# models
from backend.models.company import Executor
from backend.models.user import User, UsersValues
from backend.models.fields import Field
from backend.migrations.initial_fields import create_initial_user_fields

import json

# --- Регистрация компании и суперпользователя ---

@api_view(["POST"])
@permission_classes([AllowAny])
def register_company(request):
    data = json.loads(request.data["data"])
    print(data)

    username = None
    password = None
    company_name = None 

    searched_data = []
    for item in data:
        print(item)
        if item.get("field_id") == "username":
            username = item.get("value")
            searched_data.append(item)
        if item.get("field_id") == "password":
            password = item.get("value")
            searched_data.append(item)
        if item.get("field_id") == "company_name":
            company_name = item.get("value")
            searched_data.append(item)
        if item.get("field_id") == "company_fullName":
            company_fullName = item.get("value")
            searched_data.append(item)
    
    if not company_name:
        return Response(
            {"error": "`company_name` не задан"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Создаем компанию
    company = Executor.objects.create(
        company_name=company_name,
        company_fullName=company_fullName)
    
    # Создаем суперпользователя компании

    if not all([username, password]):
        return Response(
            {"error": "Не удалось создать пользователя - отсутствуют поля `username` или `password`"},
            status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                company=company,  # Привязываем к компании суперпользователя
                is_company_superuser=True,
                is_staff=True  # для доступа к админке если нужно
            )
        except Exception as e:
            company.delete()  # Откатываем создание компании при ошибке
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    for item in data:
        if item in searched_data:
            continue
        try:
            UsersValues.objects.create(
                id=f"{user}__{Field.objects.filter(key_name=item.get('field_id'))[0]}",
                user_id=user,
                field_id=Field.objects.filter(key_name=item.get('field_id'))[0],
                value=item.get("value", ""),
            )
        except Exception as e:
                company.delete()    # Откатываем создание компании при ошибке
                user.delete()       # Откатываем создание пользователя при ошибке
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
    
    # Автоматический логин после регистрации
    login(request, user)
    return Response({
        "status": "success",
        "company": CompanySerializer(company).data,
        "superuser": UserSerializer(user).data
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

@api_view(["GET"])
@permission_classes([AllowAny])
def get_company_fields(request):
    #create_initial_user_fields()
    company_fields = Field.objects.filter(related_item="Company")
    return Response(
        CompanyFieldSerializer(company_fields, many=True).data
    )