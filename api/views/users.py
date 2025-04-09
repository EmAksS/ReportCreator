from rest_framework.decorators import api_view, permission_classes
# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permissions import IsCompanySuperuser, IsDebug
# Serializers
from api.serializers.users import UserSerializer, UserFieldSerializer, UserFieldValueSerializer
# Response
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
# models
from backend.models.user import User, UsersValues
from backend.models.fields import Field

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
    
    if not all([username, password]):
        return Response(
            {"error": "Необходимы все поля"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            company=request.user.company,  # Привязываем к компании суперпользователя
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    required_fields = Field.objects.filter(
        related_item="User",
        is_required=True
    )

    for field in required_fields:
        if field.key_name == "password" or field.key_name == "username":
            continue
        UsersValues.objects.create(
            user=user,
            field=field,
            value=request.data.get(field.key_name, "")
        )
    
    return Response({
        "status": "success",
        "user": UserSerializer(user).data
    }, status=status.HTTP_201_CREATED)


# --- Поля для пользователей ---

@api_view(["POST"])
@permission_classes([IsCompanySuperuser|IsDebug])
def create_user_field(request):
    name = request.data.get("name")
    key_name = request.data.get("key_name")
    type = request.data.get("type")
    placeholder = request.data.get("placeholder")
    validation_regex = request.data.get("validation_regex")

    if not all([name, key_name]):
        return Response({"error": "Не указаны необходимые поля `name` или `key_name`"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        field = Field.objects.create(
            name=name,
            key_name=key_name,
            type=type,
            placeholder=placeholder,
            validation_regex=validation_regex,
            related_item="User",
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response({
        "status": "success",
        "field": UserFieldSerializer(field).data
    }, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_user_fields(request):
    # Проверяем существование обязательных полей
    if not Field.objects.filter(related_item="User").exists():   
        from backend.migrations.initial_fields import create_initial_user_fields
        create_initial_user_fields()  # Ваша функция создания полей
    
    field = Field.objects.filter(related_item="User")
    serializer = UserFieldSerializer(field, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def field_values_list(request):
    """
    Получить и/или добавить значения полей для пользователя.
    """
    if request.method == "GET":
        users_values = UsersValues.objects.filter(user=request.user)
        serializer = UserFieldValueSerializer(users_values, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = UserFieldValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def field_value_detail(request, pk):
    """
    Получить, изменить или удалить иформацию о конкретном поле `pk` для пользователя.
    """
    try:
        user_value = UsersValues.objects.get(pk=pk, user=request.user)
    except UsersValues.DoesNotExist:
        return Response({"error": "Поле не найдено"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = UserFieldValueSerializer(user_value)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = UserFieldValueSerializer(user_value, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        user_value.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# TODO: Сделать методы, которые позволяю посмотреть данные о всех пользователях.