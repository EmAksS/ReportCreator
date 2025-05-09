from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
# Serializers
from api.serializers.users import UserSerializer
from api.serializers.company import (
    CompanySerializer, 
    CompanyFieldSerializer, 
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
# autodoc
from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
    OpenApiParameter, OpenApiExample, OpenApiResponse,
)

import json

# --- Регистрация компании и суперпользователя ---


@extend_schema(tags=["Company"])
@extend_schema_view(
    get=extend_schema(
        description="Получить поля для создания компании и её суперпользователя",
        responses={
            status.HTTP_200_OK: FieldSerializer(many=True),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    ),
    post=extend_schema(
        description="Создать компанию и её суперпользователя",
        request=DataInputSerializer,
        responses={
            status.HTTP_201_CREATED: ItemDetailsSerializer,
            status.HTTP_400_BAD_REQUEST: DetailAndStatsSerializer,
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
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
        data = json.loads(json.dumps(request.data["data"]))

        error = field_validate(data, "Executor")
        if error is not None:
            return Response(DetailAndStatsSerializer(
                status=status.HTTP_400_BAD_REQUEST,
                details=f"Неправильный формат значения в поле `{error['field_id']}`."
            ), status=status.HTTP_400_BAD_REQUEST)

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
            return Response(DetailAndStatsSerializer(
                status=status.HTTP_400_BAD_REQUEST,
                details=f"Отсутствует необходимое поле `company_name`."
            ), status=status.HTTP_400_BAD_REQUEST)

        # Создаем компанию
        company = Executor.objects.create(
            company_name=company_name,
            company_fullName=company_fullName)
        
        # Создаем суперпользователя компании

        if not all([username, password]):
            return Response(DetailAndStatsSerializer(
                status=status.HTTP_400_BAD_REQUEST,
                details=f"Не удалось создать пользователя - отсутствуют поля `username` или `password`"
            ), status=status.HTTP_400_BAD_REQUEST)
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
                return Response(DetailAndStatsSerializer(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    details=f"Ошибка при создании пользователя: {str(e)}"
                ), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        for item in data:
            if item in searched_data:
                continue
            try:
                UsersValues.objects.create(
                    id=f"{str(user)}__{Field.objects.filter(key_name=item.get('field_id'), related_item='Executor')[0]}",
                    user_id=user,
                    field_id=Field.objects.filter(key_name=item.get('field_id'), related_item='Executor')[0],
                    value=item.get("value", ""),
                )
            except Exception as e:
                    company.delete()    # Откатываем создание компании при ошибке
                    user.delete()       # Откатываем создание пользователя при ошибке
                    return Response(DetailAndStatsSerializer(
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        details=f"Ошибка при создании пользователя: {str(e)}"
                    ), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Автоматический логин после регистрации
        login(request, user)
        return Response(ItemDetailsSerializer(
            status=status.HTTP_201_CREATED,
            details={
                "company": CompanySerializer(company).data,
                "superuser": UserSerializer(user).data
            }
        ), status=status.HTTP_201_CREATED)


# --- Получение информации о компании и пользователях ---


@extend_schema(tags=["Company"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить информацию о компании, в которой находится пользователь.",
        responses={
            status.HTTP_200_OK: CompanySerializer,
            status.HTTP_400_BAD_REQUEST: DetailAndStatsSerializer,
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
class CompanyInfoView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer

    def get(self, request):
        if not request.user.company:
            return Response(DetailAndStatsSerializer(
                status=status.HTTP_400_BAD_REQUEST,
                details=f"У текущего пользователя нет компании."
            ), status=status.HTTP_400_BAD_REQUEST)

        company = request.user.company
        return Response(self.serializer_class(company).data, status=status.HTTP_200_OK)


@extend_schema(tags=["Company"])
@extend_schema_view(
    get=extend_schema(
        description="Получить список пользователей компании, в которой находится пользователь.",
        responses={
            status.HTTP_200_OK: UserSerializer(many=True),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
class CompanyUsersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
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
            status.HTTP_200_OK: FieldSerializer(many=True),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    ),
    post=extend_schema(
        description="Создать заказчика компании",
        request=DataInputSerializer,
        responses={
            status.HTTP_201_CREATED: ItemDetailsSerializer,
            status.HTTP_400_BAD_REQUEST: DetailAndStatsSerializer,
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
class ContratorCreateView(generics.ListCreateAPIView):
    serializer_class = FieldSerializer
    queryset = Field.objects.filter(related_item="Contractor")
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = json.loads(json.dumps(request.data["data"]))

        error = field_validate(data, "Contractor")
        if error is not None:
            return Response(DetailAndStatsSerializer(
                status=status.HTTP_400_BAD_REQUEST,
                details=f"Неправильный формат значения в поле `{error['field_id']}`."
            ), status=status.HTTP_400_BAD_REQUEST)

        try:
            contractor = Contractor.objects.create(
                company_name = find_dataValue(data, "company_name"),
                company_fullName = find_dataValue(data, "company_fullName"),
                related_executor=request.user.company.id,
                contractor_city=find_dataValue(data, "contractor_city")
            )
        except Exception as e:
            return Response(DetailAndStatsSerializer(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    details=f"Ошибка при создании пользователя: {str(e)}"
                ), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(ItemDetailsSerializer(
            status=status.HTTP_201_CREATED,
            details=ContractorSerializer(contractor).data
        ))


@extend_schema(tags=["Contractors"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить информацию по всем заказчикам текущей компании.",
        responses={
            status.HTTP_200_OK: ContractorSerializer(many=True),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
class ContractorListView(generics.ListAPIView):
    serializer_class = ContractorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contractor.objects.filter(related_executor=self.request.user.company.id)


# --- Получение юридичеких лиц компании ---

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_executor_persons(request):
    if request.method == "GET":
        persons = ExecutorPerson.objects.filter(company=request.user.company)
        return Response(
            CompanyExecutorPersonSerializer(persons, many=True).data
        )
    
    if request.method == "POST":
        data = json.loads(json.dumps(request.data["data"]))

        error = field_validate(data, "ExecutorPerson")
        if error is not None:
            return Response({
                "error": error,
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            person = ExecutorPerson.objects.create(
                first_name=find_dataValue(data, "first_name"),
                last_name=find_dataValue(data, "last_name"),
                surname=find_dataValue(data, "surname"),
                post=find_dataValue(data, "post"),
                company=request.user.company,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            "status": "success",
            "executor_person": CompanyExecutorPersonSerializer(person).data
        })

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_contractor_persons(request):
    if request.method == "GET":
        persons = ContractorPerson.objects.filter(company=request.user.company.id)
        return Response(
            CompanyContractorPersonSerializer(persons, many=True).data
        )
    
    if request.method == "POST":
        data = json.loads(json.dumps(request.data["data"]))

        error = field_validate(data, "ExecutorPerson")
        if error is not None:
            return Response({
                "error": error,
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            contractor_id = Contractor.objects.get(id=find_dataValue(data, "company"))
        except:
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
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            "status": "success",
            "contractor_person": CompanyContractorPersonSerializer(person).data
        })
    
@api_view(["GET"])
@permission_classes([AllowAny])
def get_executor_person_fields(request):
    executor_person_fields = Field.objects.filter(related_item="ExecutorPerson")
    return Response(
        CompanyFieldSerializer(executor_person_fields, many=True).data
    )

@api_view(["GET"])
@permission_classes([AllowAny])
def get_contractor_person_fields(request):
    contractor_person_fields = Field.objects.filter(related_item="ContractorPerson")
    return Response(
        CompanyFieldSerializer(contractor_person_fields, many=True).data
    )
