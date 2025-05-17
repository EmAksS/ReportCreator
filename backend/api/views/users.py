from rest_framework import generics
from rest_framework.views import APIView
# Permissions
from rest_framework.permissions import AllowAny, IsAuthed
from api.permissions import IsCompanySuperuser, IsDebug
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
            status.HTTP_200_OK: ItemDetailsSerializer,
                #status=status.HTTP_200_OK,
                #description="Будет получен код ответа, а также информация о пользователе."
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
            status.HTTP_200_OK: FieldSerializer(many=True),
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
            status.HTTP_200_OK: ItemDetailsSerializer(
                #status=status.HTTP_200_OK,
                #description="Будет получен код ответа, а также информация о пользователе. Кроме того, пользователь станет авторизирован в системе."
            ),
            status.HTTP_400_BAD_REQUEST: DetailAndStatsSerializer(
                #status=status.HTTP_400_BAD_REQUEST,
                #details="Неверный логин и/или пароль."
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
            status.HTTP_200_OK: StatusSerializer(
                #status=status.HTTP_200_OK
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
            status.HTTP_200_OK: FieldSerializer(many=True,
                                                # related_item="User"
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
            status.HTTP_201_CREATED: ItemDetailsSerializer(
                #status=status.HTTP_201_CREATED,
                #description="Будет получен код ответа и информация о пользователе."
            ),
            status.HTTP_400_BAD_REQUEST: DetailAndStatsSerializer(
                #status=status.HTTP_400_BAD_REQUEST,
                #description="Получены неверные данные для регистрации пользователя."
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
            status.HTTP_200_OK: FieldSerializer(many=True),
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
        responses={
            status.HTTP_201_CREATED: ItemDetailsSerializer(
                #status=status.HTTP_201_CREATED,
                #detail=FieldSerializer,
                #description="Будет получен код ответа и информация о поле пользователя. Стоит обратить внимание на то, что `key_name` будет равно `key_name__company-id` после сохранения."
            ),
            status.HTTP_400_BAD_REQUEST: DetailAndStatsSerializer(
                #status=status.HTTP_400_BAD_REQUEST,
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
            status.HTTP_403_FORBIDDEN: DetailAndStatsSerializer(
                #status=status.HTTP_403_FORBIDDEN,
                #detail="Создавать поля пользователей может только суперпользователь."
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
            status.HTTP_200_OK: FieldSerializer(many=True),
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
            status.HTTP_200_OK: UserFieldValueSerializer(many=True),
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
        responses={
            status.HTTP_201_CREATED: ItemDetailsSerializer(
                #status=status.HTTP_201_CREATED,
                #detail=UserFieldValueSerializer
            ),
            status.HTTP_400_BAD_REQUEST: DetailAndStatsSerializer(
                #status=status.HTTP_400_BAD_REQUEST,
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
            status.HTTP_403_FORBIDDEN: DetailAndStatsSerializer(
                #status=status.HTTP_403_FORBIDDEN
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
            status.HTTP_404_NOT_FOUND: DetailAndStatsSerializer(
                #status=status.HTTP_404_NOT_FOUND,
                #detail="Поле не найдено"
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
        responses={
            status.HTTP_200_OK: ItemDetailsSerializer(
                #status=status.HTTP_200_OK,
                #details=UserFieldValueSerializer
            ),
            status.HTTP_400_BAD_REQUEST: DetailAndStatsSerializer(
                #status=status.HTTP_400_BAD_REQUEST,
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
            status.HTTP_404_NOT_FOUND: DetailAndStatsSerializer(
                #status=status.HTTP_404_NOT_FOUND,
                #detail="Поле не найдено"
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
            status.HTTP_204_NO_CONTENT: StatusSerializer(
                #status=status.HTTP_204_NO_CONTENT
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
            status.HTTP_404_NOT_FOUND: DetailAndStatsSerializer(
                #status=status.HTTP_404_NOT_FOUND,
                #detail="Поле не найдено"
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