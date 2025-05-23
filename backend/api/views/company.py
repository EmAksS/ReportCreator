from rest_framework import generics
# Permissions
from rest_framework.permissions import AllowAny
from api.permissions import IsAuthed, IsAuthedOrReadOnly
# Serializers
from api.serializers.users import UserSerializer
from api.serializers.company import (
    CompanySerializer,
    CompanyExecutorPersonSerializer, 
    CompanyContractorPersonSerializer,
    ContractorSerializer,
    )
from api.serializers.schema import (
    DataInputSerializer,
    StatusSerializer, 
    DetailAndStatsSerializer,
    ItemDetailsSerializer,
)
from api.serializers.field import FieldSerializer
# Response & auth
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
# models
from backend.models.company import Executor, Contractor, ExecutorPerson, ContractorPerson
from backend.models.user import User, UsersValues
from backend.models.fields import Field
# Validation
from backend.scripts.field_validate import field_validate
from backend.scripts.find_datavalue import find_dataValue
from backend.scripts.load_data import load_data
# autodoc
from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
    OpenApiExample, OpenApiResponse,
)

import json

# --- Регистрация компании и суперпользователя ---


@extend_schema(tags=["Company"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить поля создания компании",
        description="Получить поля для создания компании и её суперпользователя",
        responses={
            200: OpenApiResponse(
                response=FieldSerializer(many=True),
                description="Успешный ответ",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Получены поля для создания. Для простоты понимания структуры, показывается только один элемент поля",
                        value={
                            "data": [
                                {
                                    'name': 'Краткое название компании',
                                    'key_name': 'company_name',
                                    'is_required': True,
                                    'placeholder': 'Название компании с сокращёнными аббревиатурами',
                                    'type': 'TEXT',
                                    'validation_regex': '^[a-zA-Z0-9_\"\'\-«»а-яА-Я\s\.\,]{0,64}$',
                                    'related_item': "Executor",
                                    'related_info': None,
                                    'secure_text': False,
                                    'error_text': "Длина названия не должна превышать 64 символа, а также не содержать особых символов."
                                },
                            ]
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
        description="Создать компанию и её суперпользователя",
        request=DataInputSerializer,
        examples=[
            OpenApiExample(
                "Пример запроса",
                description="Создать компанию `reportcreator` и её суперпользователя Anon",
                value={
                    "data": [
                        { "field_id": "company_name", "value": "ИПР \"РепортКреатор\"" },
                        { "field_id": "company_fullName", "value": "Индивидуальное Программное Решение \"РепортКреатор\" (ReportCreator)" },
                        { "field_id": "username", "value": "anon" },
                        { "field_id": "password", "value": "ReportCreator1048" },
                        { "field_id": "last_name", "value": "Анонов" },
                        { "field_id": "first_name", "value": "Анон" },
                        { "field_id": "middle_name", "value": "Анонович" },
                    ]
                }
            )
        ],
        responses={
            201: OpenApiResponse(
                response=ItemDetailsSerializer,
                description="Созданы суперпользователь и компания.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={
                            "status": 201,
                            "details": {
                                "company": {
                                    "id": 123,
                                    "company_name": "ИПР \"РепортКреатор\"",
                                    "company_fullName": "Индивидуальное Программное Решение \"РепортКреатор\" (ReportCreator)",
                                    "created_at": "2025-04-24 00:00:00.00000",
                                    "updated_at": "2023-05-01 00:00:00.00000"
                                },
                                "superuser": {
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
    )
)
class CompanyRegisterView(generics.ListCreateAPIView):
    serializer_class = FieldSerializer
    queryset = Field.objects.filter(related_item="Executor")
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = load_data(request.data)

        error = field_validate(data, "Executor")
        if error is not None:
            return Response(DetailAndStatsSerializer({
                "status": status.HTTP_400_BAD_REQUEST,
                "details": f"Неправильный формат значения в поле `{error['field_id']}`."
            }).data, status=status.HTTP_400_BAD_REQUEST)

        username = None
        password = None
        company_name = None
        company_fullName = None

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
            return Response(DetailAndStatsSerializer({
                "status": status.HTTP_400_BAD_REQUEST,
                "details": f"Отсутствует необходимое поле `company_name`."
            }).data, status=status.HTTP_400_BAD_REQUEST)
        
        if not company_fullName:
            company_fullName = company_name

        if Executor.objects.filter(company_name=company_name, company_fullName=company_fullName).exists():
            return Response(DetailAndStatsSerializer({
                "status": status.HTTP_400_BAD_REQUEST,
                "details": f"Компания с таким наименованием уже существует."
            }).data, status=status.HTTP_400_BAD_REQUEST)

        # Создаем компанию
        company = Executor.objects.create(
            company_name=company_name,
            company_fullName=company_fullName)
        
        # Создаем суперпользователя компании

        if not all([username, password]):
            return Response(DetailAndStatsSerializer({
                "status": status.HTTP_400_BAD_REQUEST,
                "details": f"Не удалось создать пользователя - отсутствуют поля `username` или `password`"
            }).data, status=status.HTTP_400_BAD_REQUEST)
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
                return Response(DetailAndStatsSerializer({
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "details": f"Ошибка при создании пользователя: {str(e)}"
                }).data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        for item in data:
            if item in searched_data:
                continue
            try:
                UsersValues.objects.create(
                    id=f"{str(user)}__{Field.objects.filter(key_name=item.get('field_id'), related_item='Executor').first()}",
                    user_id=user,
                    field_id=Field.objects.filter(key_name=item.get('field_id'), related_item='Executor').first(),
                    value=item.get("value", ""),
                )
            except Exception as e:
                    company.delete()    # Откатываем создание компании при ошибке
                    user.delete()       # Откатываем создание пользователя при ошибке
                    return Response(DetailAndStatsSerializer({
                        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "details": f"Ошибка при создании пользователя: {str(e)}"
                    }
                    ).data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Автоматический логин после регистрации
        login(request, user)
        return Response(ItemDetailsSerializer({
            "status": status.HTTP_201_CREATED,
            "details": {
                "company": CompanySerializer(company).data,
                "superuser": UserSerializer(user).data
            }
        }
        ).data, status=status.HTTP_201_CREATED)


# --- Получение информации о компании и пользователях ---


@extend_schema(tags=["Company"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить информацию о компании, в которой находится пользователь.",
        responses={
            200: OpenApiResponse(
                response=CompanySerializer,
                description="Информация о компании.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        value={
                            "id": 123,
                            "company_name": "ИПР \"РепортКреатор\"",
                            "company_fullName": "Индивидуальное Программное Решение \"РепортКреатор\" (ReportCreator)",
                            "created_at": "2025-04-24 00:00:00.00000",
                            "updated_at": "2023-05-01 00:00:00.00000"
                        }
                    )
                ]
            ),
            #403:
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
class CompanyInfoView(generics.GenericAPIView):
    permission_classes = [IsAuthed]
    serializer_class = CompanySerializer

    def get(self, request):
        if not request.user.company:
            return Response(DetailAndStatsSerializer({
                "status": status.HTTP_204_NO_CONTENT,
                "details": f"У текущего пользователя нет компании."
            }).data, status=status.HTTP_204_NO_CONTENT)

        company = request.user.company
        return Response(self.serializer_class(company).data, status=status.HTTP_200_OK)


@extend_schema(tags=["Company"])
@extend_schema_view(
    get=extend_schema(
        description="Получить список пользователей компании, в которой находится пользователь.",
        responses={
            200: OpenApiResponse(
                response=UserSerializer(many=True),
                description="Список пользователей компании.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Список пользователей компании. Для простоты понимания структуры показан только один элемент списка",
                        value=[
                            {
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
class CompanyUsersView(generics.ListAPIView):
    permission_classes = [IsAuthed]
    serializer_class = UserSerializer

    def get_queryset(self):
        if not self.request.user.company:
            return []
        return User.objects.filter(company=self.request.user.company)


@extend_schema(tags=["Contractors"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список полей для создания заказчика компании",
        responses={
            200: OpenApiResponse(
                response=FieldSerializer(many=True),
                description="Список полей для создания заказчика компании.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Список полей для создания заказчика компании. Для простоты понимания структуры показан только один элемент списка",
                        value=[
                            {
                                'name': 'Краткое название компании',
                                'key_name': 'company_name',
                                'is_required': True,
                                'placeholder': 'Название компании с сокращёнными аббревиатурами',
                                'type': 'TEXT',
                                'validation_regex': '^[a-zA-Z0-9_\"\'\-«»а-яА-Я\s\.\,]{0,64}$',
                                'related_item': "Contractor",
                                'related_info': None,
                                'secure_text': False,
                                'error_text': "Длина названия не должна превышать 64 символа, а также не содержать особых символов."
                            },
                        ]
                    )
                ]
            ),
            200: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    ),
    post=extend_schema(
        description="Создать заказчика компании",
        request=DataInputSerializer,
        examples=[
            OpenApiExample(
                "Пример запроса",
                description="Создание заказчика компании",
                value={
                    "data": [
                        { "field_id": "company_name", "value": "ООО \"Аниме\"" },
                        { "field_id": "company_fullName", "value": "Общество с Ограниченной Ответственностью \"Аниме\"" },
                        { "field_id": "contractor_city", "value": "г. Москва" },
                    ]
                }
            )
        ],
        responses={
            201: OpenApiResponse(
                response=ItemDetailsSerializer,
                description="Создание заказчика компании",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Создание заказчика компании.",
                        value={
                            "status": 201,
                            "details": {
                                "id": 1,
                                "company_name": "ООО \"Аниме\"",
                                "company_fullName": "Общество с Ограниченной Ответственностью \"Аниме\"",
                                "contractor_city": "г. Москва",
                                "created_at": "2023-05-01 00:00:00.00000",
                                "updated_at": "2023-05-01 00:00:00.00000",
                            },
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
            #403:
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
class ContractorCreateView(generics.ListCreateAPIView):
    serializer_class = FieldSerializer
    queryset = Field.objects.filter(related_item="Contractor")
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = load_data(request.data)

        error = field_validate(data, "Contractor")
        if error is not None:
            return Response(DetailAndStatsSerializer({
                "status": status.HTTP_400_BAD_REQUEST,
                "details": f"Неправильный формат значения в поле `{error['field_id']}`."
            }).data, status=status.HTTP_400_BAD_REQUEST)

        try:
            contractor = Contractor.objects.create(
                company_name = find_dataValue(data, "company_name"),
                company_fullName = find_dataValue(data, "company_fullName"),
                related_executor=request.user.company,
                contractor_city=find_dataValue(data, "contractor_city")
            )
        except Exception as e:
            return Response(DetailAndStatsSerializer(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    details=f"Ошибка при создании пользователя: {str(e)}"
                ).data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(ItemDetailsSerializer({
            "status": status.HTTP_201_CREATED,
            "details": ContractorSerializer(contractor).data
        }).data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Contractors"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить информацию по всем заказчикам текущей компании.",
        responses={
            200: OpenApiResponse(
                response=ContractorSerializer(many=True),
                description="Получение списка заказчиков компании",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Список полей заказчиков текущей компании пользователя.",
                        value=[
                            {
                                "id": 1,
                                "company_name": "ООО \"Аниме\"",
                                "company_fullName": "Общество с Ограниченной Ответственностью \"Аниме\"",
                                "contractor_city": "г. Москва",
                                "created_at": "2023-07-19T17:04:23.933070Z",
                                "updated_at": "2023-07-19T17:04:23.933070Z",
                                "related_executor": {
                                    "id": 123,
                                    "company_name": "ИПР \"РепортКреатор\"",
                                    "company_fullName": "Индивидуальное Программное Решение \"РепортКреатор\" (ReportCreator)",
                                    "created_at": "2025-04-24 00:00:00.00000",
                                    "updated_at": "2023-05-01 00:00:00.00000"
                                },
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
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
class ContractorListView(generics.ListAPIView):
    serializer_class = ContractorSerializer
    permission_classes = [IsAuthed]

    def get_queryset(self):
        return Contractor.objects.filter(related_executor=self.request.user.company.id)


# --- Получение юридичеких лиц компании ---

@extend_schema(tags=["Executor Person"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить всех юридичеких лиц текущей компании.",
        responses={
            200: OpenApiResponse(
                response=CompanyExecutorPersonSerializer(many=True),
                description="Получение списка юридичеких лиц текущей компании пользователя.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Список юридичеких лиц текущей компании пользователя.",
                        value=[
                            #...
                        ]
                    )
                ]
            )
        }
    ),
    post=extend_schema(
        description="Создать юридичекого лица исполнителя текущей компании",
        request=DataInputSerializer,
        examples=[
            OpenApiExample(
                "Запрос создания юридического лица исполнителя.",
                description="Создание юридичекого лица исполнителя текущей компании",
                value={

                }
            )
        ],
        responses={
            201: OpenApiResponse(
                response=ItemDetailsSerializer,
                description="Создание юридичекого лица исполнителя компании",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Создание юридичекого лица исполнителя компании.",
                        value={
                            #...
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                #...
            ),
            401: OpenApiResponse(
                #...
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
class ExecutorPersonListCreateView(generics.ListCreateAPIView):
    serializer_class = CompanyExecutorPersonSerializer
    permission_classes = [IsAuthedOrReadOnly]

    def get_queryset(self):
        return ExecutorPerson.objects.filter(company=self.request.user.company)
    
    def create(self, request, *args, **kwargs):
        data = load_data(request.data)

        error = field_validate(data, "ExecutorPerson")
        if error is not None:
            return Response(DetailAndStatsSerializer({
                "status": status.HTTP_400_BAD_REQUEST,
                "details": f"Неправильный формат значения в поле `{error['field_id']}`."
            }).data, status=status.HTTP_400_BAD_REQUEST)

        try:
            person = ExecutorPerson.objects.create(
                first_name=find_dataValue(data, "first_name"),
                last_name=find_dataValue(data, "last_name"),
                surname=find_dataValue(data, "surname"),
                post=find_dataValue(data, "post"),
                company=request.user.company,
            )
        except Exception as e:
            return Response(DetailAndStatsSerializer({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "details": f"Ошибка при создании юридичекого лица: {str(e)}"
            }).data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(ItemDetailsSerializer({
            "status": status.HTTP_201_CREATED,
            "details": self.serializer_class(person).data
        }).data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Contractor Person"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить всех юридичеких лиц заказчиков для текущей компании.",
        responses={
            200: OpenApiResponse(
                response=CompanyContractorPersonSerializer(many=True),
                description="Получение списка юридичеких лиц заказчиков для текущей компании пользователя.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Список юридичеких лиц заказчиков для текущей компании пользователя.",
                        value=[
                            #...
                        ]
                    )
                ]
            )
        }
    ),
    post=extend_schema(
        description="Создать юридичекого лица заказчика текущей компании",
        request=DataInputSerializer,
        examples=[
            OpenApiExample(
                "Запрос создания юридического лица заказчика.",
                description="Создание юридичекого лица заказчика текущей компании",
                value={

                }
            )
        ],
        responses={
            201: OpenApiResponse(
                response=ItemDetailsSerializer,
                description="Создание юридичекого лица заказчика компании",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Создание юридичекого лица заказчика компании.",
                        value={
                            #...
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                #...
            ),
            401: OpenApiResponse(
                #...
            ),
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
class ContractorPersonListCreateView(generics.ListCreateAPIView):
    serializer_class = CompanyContractorPersonSerializer
    permission_classes = [IsAuthedOrReadOnly]

    def get_queryset(self):
        return ContractorPerson.objects.filter(company__related_executor=self.request.user.company)
    
    def create(self, request, *args, **kwargs):
        data = load_data(request.data)

        error = field_validate(data, "ContractorPerson")
        if error is not None:
            return Response(DetailAndStatsSerializer({
                "status": status.HTTP_400_BAD_REQUEST,
                "details": f"Неправильный формат значения в поле `{error['field_id']}`."
            }).data, status=status.HTTP_400_BAD_REQUEST)

        try:
            contractor_id = Contractor.objects.filter(id=int(find_dataValue(data, "company"))).first()
        except:
            return Response(
                {"error": f"Не найден заказчик с ID {find_dataValue(data, 'company')}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if contractor_id is None:
            return Response(
                {"error": f"Не найден заказчик с ID {find_dataValue(data, 'company')}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            person = ContractorPerson.objects.create(
                first_name=find_dataValue(data, "first_name"),
                last_name=find_dataValue(data, "last_name"),
                surname=find_dataValue(data, "surname"),
                post=find_dataValue(data, "post"),
                company=contractor_id,
            )
        except Exception as e:
            return Response(DetailAndStatsSerializer({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "details": f"Ошибка при создании юридичекого лица: {str(e)}"
            }).data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(ItemDetailsSerializer({
            "status": status.HTTP_201_CREATED,
            "details": self.serializer_class(person).data
        }).data, status=status.HTTP_201_CREATED)


class ExecutorPersonFieldsListView(generics.ListAPIView):
    serializer_class = FieldSerializer
    queryset = Field.objects.filter(related_item="ExecutorPerson")
    permission_classes = [AllowAny]

class ContractorPersonFieldsListView(generics.ListAPIView):
    serializer_class = FieldSerializer
    queryset = Field.objects.filter(related_item="ContractorPerson")
    permission_classes = [AllowAny]