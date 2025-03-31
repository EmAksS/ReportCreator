from rest_framework.decorators import api_view, permission_classes
# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permissions import IsCompanySuperuser
# Serializers
from api.serializers.user import UserSerializer
# Response
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
# models
from backend.models.user import User

# --- CSRF ---

@api_view(["GET"])
@permission_classes([AllowAny])
def get_csrf_token(request):
    from django.middleware.csrf import get_token
    token = get_token(request)
    return Response({"csrf_token": token})

@api_view(["GET"])
def check_auth(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response({
            "status": "authenticated",
            "user": serializer.data
        })
    return Response({"status": "not_authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

# --- Authentication ---

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        serializer = UserSerializer(user)
        return Response({
            "status": "success",
            "user": serializer.data
        })
    return Response(
        {"error": "Неправильные данные"},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"status": "success"})

# --- Регистрация обычного пользователя (только для суперпользователя компании) ---

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsCompanySuperuser])
def register_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    patronymic = request.data.get("patronymic")
    
    if not all([username, password, first_name, last_name]):
        return Response(
            {"error": "Необходимы все поля"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            company=request.user.company,  # Привязываем к компании суперпользователя
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response({
        "status": "success",
        "user": UserSerializer(user).data
    }, status=status.HTTP_201_CREATED)