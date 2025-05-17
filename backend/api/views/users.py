from rest_framework import generics
from rest_framework.views import APIView
# Permissions
from rest_framework.permissions import AllowAny
from api.permissions import IsCompanySuperuser, IsDebug, IsAuthed
# Serializers
from api.serializers.users import UserSerializer, UserFieldValueSerializer
from api.serializers.field import FieldSerializer
from api.serializers.schema import (
    DataInputSerializer,
    StatusSerializer, 
    DetailAndStatsSerializer,
    ItemDetailsSerializer,
)
# Response
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
# models
from backend.models.user import User, UsersValues
from backend.models.fields import Field
# autodoc
from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
    OpenApiParameter, OpenApiExample, OpenApiResponse,
)
# Validation
from backend.scripts.field_validate import field_validate
# scripts
from backend.scripts.find_datavalue import find_dataValue

import json

# --- CSRF ---

@extend_schema(tags=['Auth'])
@extend_schema_view(
    get=extend_schema(
        summary="Получить текущий CSRF-токен.",
        responses={
            200: OpenApiResponse(
                response=DetailAndStatsSerializer,
                description="Будет получен код ответа и текущий CSRF-токен.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Содержит код ответа и CSRF-токен.",
                        value={
                            'status': status.HTTP_200_OK,
                            'details': 'csrf_token'
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
                ),
        }
    )
)
class CsrfView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        from django.middleware.csrf import get_token
        token = get_token(request)
        return Response(DetailAndStatsSerializer({
            'status': status.HTTP_200_OK,
            'details': token
        }).data, status=status.HTTP_200_OK)


@extend_schema(tags=['Auth'])
@extend_schema_view(
    get=extend_schema(
        summary="Проверить статус аутентификации текущего пользователя в системе.",
        responses={
            200: OpenApiResponse(
                response=ItemDetailsSerializer,
                description="Будет получен код ответа и информация о пользователе.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Содержит код ответа и информацию о пользователе.",
                        value={
                            'status': status.HTTP_200_OK,
                            'details': {
                                "username": "anon",
                                "company": {
                                    "id": 123,
                                    "company_name": "ИПР \"РепортКреатор\"",
                                    "company_fullName": "Индивидуальное Программное Решение \"РепортКреатор\" (ReportCreator)",
                                    "created_at": "2025-04-24 00:00:00.00000",
                                    "updated_at": "2023-05-01 00:00:00.00000"
                                },
                                "is_company_superuser": True,
                            }
                        }
                    )
                ]
            ),
            401: OpenApiResponse(
                response=StatusSerializer,
                description="Пользователь неавторизирован в системе",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Пользователь неавторизирован в системе",
                        value={
                            "status": 401
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
class AuthCheckView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        print(request.user)
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(ItemDetailsSerializer({
                'status': status.HTTP_200_OK,
                'details': serializer.data
            }).data, status=status.HTTP_200_OK)
        else:
            return Response(StatusSerializer(
                {'status': status.HTTP_401_UNAUTHORIZED},
            ).data, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(tags=['Auth'])
@extend_schema_view(
    get=extend_schema(
        summary="Получить поля для аутентификации пользователя",
        responses={
            200: OpenApiResponse(
                response=FieldSerializer(many=True),
                description="Будет получен список полей для аутентификации пользователя.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Содержит список полей для аутентификации пользователя. Для удобства понимания информации показывается только один элемент списка.",
                        value=[
                            {
                                'name': 'Логин',
                                'key_name': 'username',
                                'is_required': True,
                                'placeholder': 'Ваш логин пользователя',
                                'type': 'TEXT',
                                'validation_regex': '^[a-zA-Z0-9_-]{4,16}$',
                                'related_item': "User",
                                'related_info': None,
                                'secure_text': False,
                                'error_text': "Имя пользователя должно быть уникальным, не должно содержать пробелов и быть от 4 до 16 символов.",
                            },
                        ]
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    ),
    post=extend_schema(
        summary="Выполнить аутентификацию пользователя в систему.",
        request=DataInputSerializer,
        responses={
            200: OpenApiResponse(
                response=ItemDetailsSerializer,
                description="Будет получен код ответа и информация о пользователе.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Содержит код ответа и информацию о пользователе.",
                        value={
                            'status': status.HTTP_200_OK,
                            'details': {
                                "username": "anon",
                                "company": {
                                    "id": 123,
                                    "company_name": "ИПР \"РепортКреатор\"",
                                    "company_fullName": "Индивидуальное Программное Решение \"РепортКреатор\" (ReportCreator)",
                                    "created_at": "2025-04-24 00:00:00.00000",
                                    "updated_at": "2023-05-01 00:00:00.00000"
                                },
                                "is_company_superuser": True,
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                response=DetailAndStatsSerializer,
                description="Неправильные данные",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Неправильные данные в теле запроса. Текст ошибки может отличаться.",
                        value={
                            "status": 400,
                            "details": "Текст ошибки"
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    ),
)
class UserAuthView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Field.objects.filter(related_item="User")
    serializer_class = FieldSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(json.dumps(request.data["data"]))

        username = find_dataValue(data, "username")
        password = find_dataValue(data, "password")

        print(f"Пользователь {username} входит в систему под паролем {password}")

        user = authenticate(request, username=username, password=password)
        
        if user is None:
            return Response(DetailAndStatsSerializer({
                'status': status.HTTP_400_BAD_REQUEST,
                'details': "Неверный логин и/или пароль."
            }).data, status=status.HTTP_400_BAD_REQUEST)
        
        login(request, user)

        print(request.user)
        
        serializer = UserSerializer(user)
        return Response(ItemDetailsSerializer({
            'status': status.HTTP_200_OK,
            'details': serializer.data
        }).data, status=status.HTTP_200_OK)


@extend_schema(tags=['Auth'])
@extend_schema_view(
    post=extend_schema(
        summary="Выполнить выход из ситемы для текущего пользователя системы.",
        responses={
            200: OpenApiResponse(
                response=StatusSerializer,
                description="Будет получен код ответа и выполнен выход из системы.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Будет получен код ответа и выполнен выход из системы.",
                        value={
                            'status': status.HTTP_200_OK,
                        }
                    )
                ]
            ),
            401: OpenApiResponse(
                response=StatusSerializer,
                description="Пользователь неавторизирован в системе",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Пользователь неавторизирован в системе",
                        value={
                            "status": 401
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
class UserLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(StatusSerializer(
                {'status': status.HTTP_401_UNAUTHORIZED},
            ).data, status=status.HTTP_401_UNAUTHORIZED)

        logout(request)
        return Response(StatusSerializer(
                {'status': status.HTTP_200_OK},
            ).data, status=status.HTTP_200_OK)


@extend_schema(tags=['Auth'])
@extend_schema_view(
    get=extend_schema(
        summary="Получить поля для регистрации пользователя суперпользователем.",
        responses={
            200: OpenApiResponse(
                response=FieldSerializer(many=True),
                description="Будет получен список полей для регистрации пользователя.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Содержит список полей для регистрации пользователя суперпользователем. Для понимаия структуры, выведен только один элемент списка.",
                        value=[
                            {
                                'name': 'Логин',
                                'key_name': 'username',
                                'is_required': True,
                                'placeholder': 'Ваш логин пользователя',
                                'type': 'TEXT',
                                'validation_regex': '^[a-zA-Z0-9_-]{4,16}$',
                                'related_item': "User",
                                'related_info': None,
                                'secure_text': False,
                                'error_text': "Имя пользователя должно быть уникальным, не должно содержать пробелов и быть от 4 до 16 символов.",
                            },
                        ]
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    ),
    post=extend_schema(
        summary="Выполнить регистрацию пользователя в системе.",
        request=DataInputSerializer,
        responses={
            201: OpenApiResponse(
                response=ItemDetailsSerializer,
                description="Будет получен код ответа и информация о созданном пользователе.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Содержит код ответа и информацию о пользователе.",
                        value={
                            'status': status.HTTP_201_CREATED,
                            'details': {
                                "username": "anon",
                                "company": {
                                    "id": 123,
                                    "company_name": "ИПР \"РепортКреатор\"",
                                    "company_fullName": "Индивидуальное Программное Решение \"РепортКреатор\" (ReportCreator)",
                                    "created_at": "2025-04-24 00:00:00.00000",
                                    "updated_at": "2023-05-01 00:00:00.00000"
                                },
                                "is_company_superuser": True,
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                response=DetailAndStatsSerializer,
                description="Неправильные данные",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Получены неверные данные для регистрации пользователя.",
                        value={
                            "status": 400,
                            "details": "Текст ошибки"
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    ),
)
class UserRegisterView(generics.CreateAPIView):
    queryset = Field.objects.filter(related_item="User")
    serializer_class = FieldSerializer
    permission_classes = [IsCompanySuperuser]

    def post(self, request, *args, **kwargs):
        data = json.loads(json.dumps(request.data["data"]))

        error = field_validate(data)
        if error is not None:
            return Response(DetailAndStatsSerializer({
                'status': status.HTTP_400_BAD_REQUEST,
                'details': "Ошибка валидации значения: не пройдена валидация поля {error.get('field_id')}"
            }).data, status=status.HTTP_400_BAD_REQUEST)

        username = find_dataValue(data, "username")
        password = find_dataValue(data, "password")

        if not all([username, password]):
            return Response(DetailAndStatsSerializer({
                'status': status.HTTP_400_BAD_REQUEST,
                'details': "Не удалось создать пользователя - отсутствуют поля `username` или `password`"
            }).data, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    company=request.user.company,  # Привязываем к компании суперпользователя
                    is_company_superuser=False,
                    is_staff=False  # для доступа к админке если нужно
                )
            except Exception as e:
                return Response(DetailAndStatsSerializer({
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'details': f"Внутренняя ошибка сервера: {e}"
                }).data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        for item in data:
            if item.get("field_id") in ["username", "password"]:
                continue
            try:
                UsersValues.objects.create(
                    id=f"{user}__{Field.objects.filter(key_name=item.get('field_id'), related_item='User')[0]}",
                    user_id=user,
                    field_id=Field.objects.filter(key_name=item.get('field_id', related_item='User'))[0],
                    value=item.get("value", ""),
                )
            except Exception as e:
                    user.delete()   # Удаляем пользователя, если произошла ошибка
                    return Response(DetailAndStatsSerializer({
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'details': f"Внутренняя ошибка сервера: {e}"
                    }).data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(ItemDetailsSerializer({
            'status': status.HTTP_201_CREATED,
            'details': UserSerializer(user).data
        }), status=status.HTTP_201_CREATED)


# --- Поля для пользователей ---


@extend_schema(tags=['User Fields'])
@extend_schema_view(
    get=extend_schema(
        summary="Получить поля для создания нового поля пользователя.",
        responses={
            200: OpenApiResponse(
                response=FieldSerializer(many=True),
                description="Будет получен список полей для создания полей пользователя.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Содержит список полей для создания кастомный полей пользователя. Для понимаия структуры, выведен только один элемент списка.",
                        value=[
                            {
                                'name': 'Русское название поля',
                                'key_name': 'name',
                                'is_required': True,
                                'placeholder': 'Введите русское название поля',
                                'type': 'TEXT',
                                'validation_regex': '^[а-яА-Я]+(-[а-яА-Я]+)*{0,64}$',
                                'related_item': "Field",
                                'related_info': None,
                                'secure_text': False,
                                'error_text': "Значение должно содержать только кириллицу, а также не более 64 символов",
                            },
                        ]
                    )
                ]
            ),
            401: OpenApiResponse(
                response=StatusSerializer,
                description="Пользователь неавторизирован в системе",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Пользователь неавторизирован в системе",
                        value={
                            "status": 401
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    ),
    post=extend_schema(
        summary="Создать новое поле пользователя. Может выполнять только суперпользователь",
        request=DataInputSerializer,
        examples=[
            OpenApiExample(
                "Пример запроса",
                description="Создание нового поля пользователя. Пример запроса с параметром `data` в теле запроса.",
                value={
                    "data": [
                        { "field_id": "name", "value": "Образование пользователя" },
                        { "field_id": "key_name", "value": "education" },
                        { "field_id": "is_required", "value": True },
                        { "field_id": "placeholder", "value": "Введите образование пользователя" },
                        { "field_id": "type", "value": "TEXT" },
                        { "field_id": "validation_regex", "value": None },
                        { "field_id": "error_text", "value": "Не введено образование!" },
                    ]
                }
            )
        ],
        responses={
            201: OpenApiResponse(
                response=ItemDetailsSerializer,
                description="Будет получен объект созданного поля пользователя.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Создано поле пользователя.",
                        value={
                            'status': status.HTTP_201_CREATED,
                            'details': {
                                "id": 1,
                                "name": "Образование пользователя",
                                "key_name": "education__1",
                                "related_item": "User",
                                "related_info": None,
                                "error_text": "Не введено образование!",
                                "is_required": True,
                                "placeholder": "Введите образование пользователя",
                                "type": "TEXT",
                                "validation_regex": None,
                                "secure_text": False,
                                "is_custom": True,
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                response=DetailAndStatsSerializer,
                description="Неправильные данные",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Неправильные данные в теле запроса. Текст ошибки может отличаться.",
                        value={
                            "status": 400,
                            "details": "Текст ошибки"
                        }
                    )
                ]
            ),
            401: OpenApiResponse(
                response=StatusSerializer,
                description="Пользователь неавторизирован в системе",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Пользователь неавторизирован в системе",
                        value={
                            "status": 401
                        }
                    )
                ]
            ),
            403: OpenApiResponse(
                response=DetailAndStatsSerializer,
                description="Доступ запрещен",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Доступ запрещен",
                        value={
                            "status": 403,
                            "details": "Создавать поля пользователей может только суперпользователь."
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
class UserFieldListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthed]
    
    def get(self, request):
        from .field import FieldFieldsListView
        return FieldFieldsListView.as_view()(request._request)

    def create(self, request, *args, **kwargs):
        if not request.user.is_company_superuser:
            return Response(DetailAndStatsSerializer({
                'status': status.HTTP_403_FORBIDDEN,
                'details': "Создавать поля пользователей может только суперпользователь."
            }), status=status.HTTP_403_FORBIDDEN)
        
        data = json.loads(json.dumps(request.data["data"]))

        error = field_validate(data)
        if error is not None:
            return Response(DetailAndStatsSerializer({
                'status': status.HTTP_400_BAD_REQUEST,
                'details': f"Ошибка валидации значения: не пройдена валидация поля {error.get('field_id')}"
            }), status=status.HTTP_400_BAD_REQUEST)
        
        name = find_dataValue(data, "name")
        key_name = find_dataValue(data, "key_name")
        type = find_dataValue(data, "type")
        placeholder = find_dataValue(data, "placeholder")
        validation_regex = find_dataValue(data, "validation_regex")

        if not all([name, key_name, type]):
            return Response(DetailAndStatsSerializer({
                'status': status.HTTP_400_BAD_REQUEST,
                'details': "Не удалось создать поле пользователя - отсутствуют поля `name`, `key_name` или `type`"
            }), status=status.HTTP_400_BAD_REQUEST)
        
        try:
            field = Field.objects.create(
                id=f"{key_name}__User",
                name=name,
                key_name=f"{key_name}__{request.user.company.id}",
                type=type,
                placeholder=placeholder,
                validation_regex=validation_regex,
                related_item="User",
                is_custom=True,
            )
        except Exception as e:
            return Response(DetailAndStatsSerializer({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'details': f"Внутренняя ошибка сервера: {e}"
            }), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(ItemDetailsSerializer({
            'status': status.HTTP_201_CREATED,
            'details': FieldSerializer(field).data
        }), status=status.HTTP_201_CREATED)


@extend_schema(tags=['User Fields'])
@extend_schema_view(
    get=extend_schema(
        summary="Получить все кастомные поля для текущей компании.",
        responses={
            200: OpenApiResponse(
                response=FieldSerializer(many=True),
                description="Будет получен список кастомный полей пользователя.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Содержит список кастомный полей пользователя. Для понимаия структуры, выведен только один элемент списка.",
                        value=[
                            {
                                "id": 1,
                                "name": "Образование пользователя",
                                "key_name": "education__1",
                                "related_item": "User",
                                "related_info": None,
                                "error_text": "Не введено образование!",
                                "is_required": True,
                                "placeholder": "Введите образование пользователя",
                                "type": "TEXT",
                                "validation_regex": None,
                                "secure_text": False,
                                "is_custom": True,
                            },
                        ]
                    )
                ]
            ),
            401: OpenApiResponse(
                response=StatusSerializer,
                description="Пользователь неавторизирован в системе",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Пользователь неавторизирован в системе",
                        value={
                            "status": 401
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
class UserCustomFieldsView(generics.ListAPIView):
    serializer_class = FieldSerializer
    permission_classes = [IsAuthed]

    def get(self, request):
        fields = Field.objects.filter(id__endswith=f"__{request.user.company.id}", is_custom=True, related_item="User")
        return Response(self.serializer_class(fields, many=True).data, status=status.HTTP_200_OK)


@extend_schema(tags=['User Fields Value'])
@extend_schema_view(
    get=extend_schema(
        summary="Получить все значения полей текущего пользователя.",
        responses={
            200: OpenApiResponse(
                response=UserFieldValueSerializer(many=True),
                description="Будет получен список значений полей пользователя.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Содержит список значений полей пользователя. Для простоты понимания структуры выведен только один элемент списка.",
                        value=[
                            {
                                "id": "username__key_name",
                                "value": "КФУ",
                                "field_id": {
                                    "id": "education__1__User",
                                    "name": "Образование пользователя",
                                    "key_name": "education__1",
                                    "related_item": "User",
                                    "related_info": None,
                                    "error_text": "Не введено образование!",
                                    "is_required": True,
                                    "placeholder": "Введите образование пользователя",
                                    "type": "TEXT",
                                    "validation_regex": None,
                                    "secure_text": False,
                                    "is_custom": True,
                                },
                                "user_id": {
                                    "username": "anon",
                                    "company": {
                                        "id": 123,
                                        "company_name": "ИПР \"РепортКреатор\"",
                                        "company_fullName": "Индивидуальное Программное Решение \"РепортКреатор\" (ReportCreator)",
                                        "created_at": "2025-04-24 00:00:00.00000",
                                        "updated_at": "2023-05-01 00:00:00.00000"
                                    },
                                    "is_company_superuser": True,
                                },
                                "created_at": "2023-08-18T11:55:44.826260+03:00",
                                "updated_at": "2023-08-18T11:55:44.826260+03:00"
                            }
                        ]
                    )
                ]
            ),
            401: OpenApiResponse(
                response=StatusSerializer,
                description="Пользователь неавторизирован в системе",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Пользователь неавторизирован в системе",
                        value={
                            "status": 401
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    ),
    post=extend_schema(
        summary="Создать новое значение поля пользователя.",
        request=DataInputSerializer,
        examples=[
            OpenApiExample(
                "Пример запроса",
                description="Запрос на создание нового значения поля пользователя.",
                value={
                    "data": [
                        { 'field_id': 'user_id', 'value': 'anon' },
                        { 'field_id': 'field_id', 'value': 'education__1__User' },
                        { 'field_id': 'value', 'value': 'КФУ' }
                    ]
                }
            )
        ],
        responses={
            201: OpenApiResponse(
                response=ItemDetailsSerializer,
                description="Будет создано новое значение поля пользователя.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Будет создано новое значение поля пользователя.",
                        value={
                            "status": 201,
                            "details": {
                                "id": "username__key_name",
                                "value": "КФУ",
                                "field_id": {
                                    "id": 1,
                                    "name": "Образование пользователя",
                                    "key_name": "education__1",
                                    "related_item": "User",
                                    "related_info": None,
                                    "error_text": "Не введено образование!",
                                    "is_required": True,
                                    "placeholder": "Введите образование пользователя",
                                    "type": "TEXT",
                                    "validation_regex": None,
                                    "secure_text": False,
                                    "is_custom": True,
                                },
                                "user_id": {
                                    "username": "anon",
                                    "company": {
                                        "id": 123,
                                        "company_name": "ИПР \"РепортКреатор\"",
                                        "company_fullName": "Индивидуальное Программное Решение \"РепортКреатор\" (ReportCreator)",
                                        "created_at": "2025-04-24 00:00:00.00000",
                                        "updated_at": "2023-05-01 00:00:00.00000"
                                    },
                                    "is_company_superuser": True,
                                },
                                "created_at": "2023-08-18T11:55:44.826260+03:00",
                                "updated_at": "2023-08-18T11:55:44.826260+03:00"
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                response=DetailAndStatsSerializer,
                description="Неправильные данные",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Неправильные данные в теле запроса. Текст ошибки может отличаться.",
                        value={
                            "status": 400,
                            "details": "Текст ошибки"
                        }
                    )
                ]
            ),
            401: OpenApiResponse(
                response=StatusSerializer,
                description="Пользователь неавторизирован в системе",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Пользователь неавторизирован в системе",
                        value={
                            "status": 401
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
class UserFieldValueView(generics.ListCreateAPIView):
    serializer_class = UserFieldValueSerializer
    permission_classes = [IsAuthed]

    def get(self, request):
        users_values = UsersValues.objects.filter(user_id=request.user)
        return Response(self.serializer_class(users_values, many=True).data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        data = json.loads(json.dumps(request.data["data"]))

        error = field_validate(data)
        if error is not None:
            return Response(DetailAndStatsSerializer({
            'status': status.HTTP_400_BAD_REQUEST,
            'details': f"Ошибка валидации значения: не пройдена валидация поля {error.get('field_id')}"
        }), status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(
            field_id=find_dataValue(data, "field_id"),
            user_id=request.user,
            value=find_dataValue(data, "value"))
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(ItemDetailsSerializer({
                'status': status.HTTP_201_CREATED,
                'details': serializer.data
            }), status=status.HTTP_201_CREATED)

        return Response(DetailAndStatsSerializer({
            'status': status.HTTP_400_BAD_REQUEST,
            'details': "Ошибка валидации данных при сохранении значения поля пользователя."
        }), status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['User Fields Value'])
@extend_schema_view(
    get=extend_schema(
        summary="Получить значение поля `pk` текущего пользователя.",
        responses={
            status.HTTP_200_OK: UserFieldValueSerializer,
            200: OpenApiResponse(
                response=UserFieldValueSerializer,
                description="Получить значение поля пользователя.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Получить значение поля пользователя.",
                        value={
                            "status": 200,
                            "details": {
                                "id": "username__key_name",
                                "value": "КФУ",
                                "field_id": {
                                    "id": 1,
                                    "name": "Образование пользователя",
                                    "key_name": "education__1",
                                    "related_item": "User",
                                    "related_info": None,
                                    "error_text": "Не введено образование!",
                                    "is_required": True,
                                    "placeholder": "Введите образование пользователя",
                                    "type": "TEXT",
                                    "validation_regex": None,
                                    "secure_text": False,
                                    "is_custom": True,
                                },
                                "user_id": {
                                    "username": "anon",
                                    "company": {
                                        "id": 123,
                                        "company_name": "ИПР \"РепортКреатор\"",
                                        "company_fullName": "Индивидуальное Программное Решение \"РепортКреатор\" (ReportCreator)",
                                        "created_at": "2025-04-24 00:00:00.00000",
                                        "updated_at": "2023-05-01 00:00:00.00000"
                                    },
                                    "is_company_superuser": True,
                                },
                                "created_at": "2023-08-18T11:55:44.826260+03:00",
                                "updated_at": "2023-08-18T11:55:44.826260+03:00"
                            }
                        }
                    )
                ]
            ),
            401: OpenApiResponse(
                response=StatusSerializer,
                description="Пользователь неавторизирован в системе",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Пользователь неавторизирован в системе",
                        value={
                            "status": 401
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                response=DetailAndStatsSerializer,
                description="Поле не найдено",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Поле не найдено",
                        value={
                            "status": 404,
                            "details": "Поле не найдено"
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    ),
    put=extend_schema(
        summary="Обновить значение поля пользователя.",
        request=DataInputSerializer,
        examples=[
            OpenApiExample(
                "Пример запроса",
                description="Обновить значение поля `value` пользователя.",
                value={
                    "data": [
                        { "field_id": "value", "value": "КФУ" }
                    ]
                }
            )
        ],
        responses={
            200: OpenApiResponse(
                response=UserFieldValueSerializer,
                description="Получить значение обновлённых полей.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Получить значение поля пользователя (обновлено только value).",
                        value={
                            "status": 200,
                            "details": {
                                "id": "username__key_name",
                                "value": "КФУ",
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                response=DetailAndStatsSerializer,
                description="Неправильные данные",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Неправильные данные в теле запроса. Текст ошибки может отличаться.",
                        value={
                            "status": 400,
                            "details": "Текст ошибки"
                        }
                    )
                ]
            ),
            401: OpenApiResponse(
                response=StatusSerializer,
                description="Пользователь неавторизирован в системе",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Пользователь неавторизирован в системе",
                        value={
                            "status": 401
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                response=DetailAndStatsSerializer,
                description="Поле не найдено",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Поле не найдено",
                        value={
                            "status": 404,
                            "details": "Поле не найдено"
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    ),
    delete=extend_schema(
        summary="Удалить значение поля пользователя.",
        responses={
            204: OpenApiResponse(
                response=StatusSerializer,
                description="Значение поля пользователя успешно удалено.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Значение поля успешно удалено",
                        value={
                            "status": 204
                        }
                    )
                ]
            ),
            401: OpenApiResponse(
                response=StatusSerializer,
                description="Пользователь неавторизирован в системе",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Пользователь неавторизирован в системе",
                        value={
                            "status": 401
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                response=DetailAndStatsSerializer,
                description="Поле не найдено",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Поле не найдено",
                        value={
                            "status": 404,
                            "details": "Поле не найдено"
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
class UserFieldValueDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserFieldValueSerializer
    permission_classes = [IsAuthed]

    def __get_user_value(self, pk, user):
        try:
            return UsersValues.objects.get(pk=pk, user_id=user)
        except UsersValues.DoesNotExist:
            return Response(DetailAndStatsSerializer({
                'status': status.HTTP_404_NOT_FOUND,
                'details': "Поле не найдено"
            }), status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        value = self.__get_user_value(kwargs.get("pk"), request.user)
        serializer = self.serializer_class(value)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        value = self.__get_user_value(kwargs.get("pk"), request.user)

        data = json.loads(json.dumps(request.data["data"]))
        error = field_validate(data)
        if error is not None:
            return Response(DetailAndStatsSerializer({
                'status': status.HTTP_400_BAD_REQUEST,
                'details': f"Ошибка валидации значения: не пройдена валидация поля {error.get('field_id')}"
            }).data, status=status.HTTP_400_BAD_REQUEST)
        
        to_change = {}
        for item in data:
            to_change[item["field_id"]] = item["value"]

        serializer = self.serializer_class(
            value,
            **to_change,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(ItemDetailsSerializer({
                'status': status.HTTP_200_OK,
                'details': serializer.data
            }).data, status=status.HTTP_200_OK)
        return Response(DetailAndStatsSerializer({
            'status': status.HTTP_400_BAD_REQUEST,
            'details': "Ошибка валидации данных при сохранении значения поля пользователя."
        }), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        value = self.__get_user_value(kwargs.get("pk"), request.user)
        value.delete()
        return Response(StatusSerializer(
            {'status': status.HTTP_204_NO_CONTENT}
        ).data, status=status.HTTP_204_NO_CONTENT)


# TODO: Сделать методы, которые позволяю посмотреть данные о всех пользователях.