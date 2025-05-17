from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
# Permissions
from rest_framework import permissions
from api.permissions import IsCompanySuperuser, IsDebug
# models 
from backend.models.fields import Field
from backend.models.documents import Template, Document, DocumentField
from backend.models.company import ContractorPerson, ExecutorPerson 
# autodocs
from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
    OpenApiParameter, OpenApiExample, OpenApiResponse,
)
# serializers
from api.serializers.documents import (
    TemplateSerializer,
    DocumentSerializer,
    DocumentFieldSerializer,
    DocumentFieldValueSerializer,
)
from api.serializers.field import FieldSerializer
from api.serializers.schema import (
    DataInputSerializer,
    StatusSerializer, 
    DetailAndStatsSerializer,
    ItemDetailsSerializer,
)
# scripts
from backend.scripts.field_validate import field_validate
import json
from backend.scripts.find_datavalue import find_dataValue
# file settings
from django.conf import settings
import os
#from magic import Magic

# region DocTypes_docs
@extend_schema(tags=["Documents"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список типов документов для создания",
    ),
    responses = {
        status.HTTP_200_OK: OpenApiResponse
    }
)
# endregion
class DocumentTypesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response([
        {
            "code": "ACT",
            "name": "Акт"
        },
        {
            "code": "ORDER",
            "name": "Заказ"
        },
        {
            "code": "REPORT",
            "name": "Отчёт"
        }
    ])


# region Templates_docs
@extend_schema(tags=["Template"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список полей для создания шаблона документа",
        responses={
            200: OpenApiResponse(
                response=FieldSerializer(many=True),
                description="Список полей для создания шаблона документа",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Список полей для создания шаблона документа. Для понимания структуры показан только один элемент списка.",
                        value=[
                            {
                                'name': 'Тип документа',
                                'key_name': 'template_type',
                                'is_required': True,
                                'placeholder': 'Выберите тип создаваемого документа',
                                'type': 'COMBOBOX',
                                'validation_regex': None,
                                'related_item': "Template",
                                'related_info': {
                                    'url': "document/types/",
                                    'show_field': "name",
                                    'save_field': "code",
                                },
                                'secure_text': False,
                                'error_text': ""
                            },
                        ]
                    )
                ]
            )
        }
    ),
    post=extend_schema(
        summary="Создать шаблон документа",
        request=DataInputSerializer,
        examples=[
            OpenApiExample(
                "Пример запроса",
                summary="Пример запроса",
                value={
                    "data": [
                        { "field_id": "template_name", "value": "Аниме_Акт_1" },
                        { "field_id": "template_file", "value": "TODO: понять как передаётся файл" },
                        { "field_id": "template_type", "value": "один из `document/types/`" },
                        { "field_id": "related_executor_person", "value": 12 },
                        { "field_id": "related_contractor_person", "value": 4 },
                    ]
                }
            )
        ],
        responses={
            201: OpenApiResponse(
                response=ItemDetailsSerializer,
                description="Создан шаблон документа",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        summary="Создан шаблон документа",
                        description="Создан шаблон документа",
                        value={
                            "status": 201,
                            "details": {
                                "id": 1,
                                "name": "Аниме_Акт_1",
                                "type": "ACT",
                                "template_file": "?????????????",
                                "related_contractor_person": {
                                    "todo": "contractor_person_documentation"
                                },
                                "related_executor_person": {
                                    "todo": "executor_person_documentation"
                                }
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
                description="Доступ запрещён",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Пользователю запрещён метод. Текст ошибки может отличаться.",
                        value={
                            "status": 403,
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
# endregion
class TemplateListCreateView(generics.ListCreateAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request, *args, **kwargs):
        return TemplateFieldsView.as_view()(request._request)

    def create(self, request, *args, **kwargs):
        data = json.loads(json.dumps(request.data["data"]))

        error = field_validate(data, "Template")
        if error is not None:
            return Response(DetailAndStatsSerializer({
                "status": status.HTTP_400_BAD_REQUEST,
                "details": f"Неправильный формат значения в поле `{error['field_id']}`."
            }).data, status=status.HTTP_400_BAD_REQUEST)
        
        # Загрузка документа
        uploaded_file = request.FILES['template_file']
        upload_dir = settings.TEMPLATES_FOLDER

        # Проверяем расширение .docx
        if not uploaded_file.name.lower().endswith('.docx'):
            return Response(DetailAndStatsSerializer({
                "status": status.HTTP_400_BAD_REQUEST,
                "details": f"Файл должен быть в формат *.docx."
            }).data, status=status.HTTP_400_BAD_REQUEST)

        # TODO # Проверяем MIME-тип (дополнительная защита)
        # mime = Magic(mime=True)
        # file_mime_type = mime.from_buffer(uploaded_file.read(1024))
        # uploaded_file.seek(0)  # Возвращаем курсор в начало файла

        # if file_mime_type != 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        #     return Response(DetailAndStatsSerializer(
        #         status=status.HTTP_400_BAD_REQUEST,
        #         details=f"Файл должен быть в формат *.docx."
        #     ), status=status.HTTP_400_BAD_REQUEST)

        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        file_path = os.path.join(upload_dir, uploaded_file.name)
        
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Проверка юридических лиц

        try: 
            contractor = ContractorPerson.objects.get(id=find_dataValue(data, 'related_contractor_person'))
        except:
            return Response(DetailAndStatsSerializer({
                'status': status.HTTP_400_BAD_REQUEST,
                'details': f"Не найдено юридическое лицо заказчика с ID {find_dataValue(data, 'related_contractor_person')}"
            }).data, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            executor = ExecutorPerson.objects.get(id=find_dataValue(data, 'related_executor_person'))
        except:
            return Response(DetailAndStatsSerializer({
                'status': status.HTTP_400_BAD_REQUEST,
                'details': f"Не найдено юридическое лицо исполнителя с ID {find_dataValue(data, 'related_executor_person')}"
            }).data, status=status.HTTP_400_BAD_REQUEST)

        try:
            template = Template(
                name=find_dataValue(data, 'name'),
                type=find_dataValue(data, 'type'),
                file=file_path,
                related_contractor_person=contractor,
                related_executor_person=executor,
            )
        except Exception as e:
            return Response(DetailAndStatsSerializer({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'details': f"Ошибка создания объекта модели `Template`. {e}"
            }).data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        template.save()
        return Response(ItemDetailsSerializer({
            "status": status.HTTP_201_CREATED,
            "details": TemplateSerializer(template).data,
        }).data, status=status.HTTP_201_CREATED)


# region DocumentFields_docs
@extend_schema(tags=["DocumentField"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список полей для создания документа с ID шаблона `TID`",
        parameters=[
            OpenApiParameter(
                "tid",
                type=int,
                location=OpenApiParameter.PATH,
            description="ID шаблона документа"),
        ],
        responses={
            200: OpenApiResponse(
                response=DocumentFieldSerializer(many=True),
                description="Список полей для создания поля для документа",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Список полей для создания поля для документа. Для простоты понимания структуры показан только один элемент списка.",
                        value=[
                            {
                                'name': 'Русское название поля',
                                'key_name': 'name',
                                'is_required': True,
                                'placeholder': 'Введите русское название поля',
                                'type': 'TEXT',
                                'validation_regex': '^[а-яА-Я]+(-[а-яА-Я]+)*{0,64}$',
                                'related_item': "DocumentField",
                                'related_info': None,
                                'secure_text': False,
                                'error_text': "Значение должно содержать только кириллицу, а также не более 64 символов"
                            },
                        ]
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
            403: OpenApiResponse(
                response=StatusSerializer,
                description="Доступ запрещён",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Пользователю запрещён метод.",
                        value={
                            "status": 403,
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
        summary="Создать новое поле для документа",
        request=DataInputSerializer,
        examples=[
            OpenApiExample(
                "Пример запроса",
                description="Пример создания поля документа с `TID=1`",
                value={
                    "data": [
                        { "field_id": "name", "value" : "Название договора" },
                        { "field_id": "related_template", "value" : 1 },
                        { "field_id": "key_name", "value" : "dogovor_name" },
                        { "field_id": "is_required", "value" : True },
                        { "field_id": "validation_regex", "value" : None },
                        { "field_id": "type", "value" : 4 },
                        { "field_id": "placeholder", "value" : "Название договора" },
                        { "field_id": "error_text", "value" : None },
                    ]
                },
                status_codes=[
                    str(status.HTTP_201_CREATED),
                    str(status.HTTP_400_BAD_REQUEST),
                ],
                request_only=True,
        )
        ],
        responses={
            201: OpenApiResponse(
                response=ItemDetailsSerializer,
                description="Создано новое поле для документа",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Создано новое поле для документа.",
                        value={
                            "status": 201,
                            "details": {
                                'name': 'Название договора',
                                'key_name': '1__dogovor_name',
                                'is_required': True,
                                'placeholder': 'Название договора',
                                'type': 'TEXT',
                                'validation_regex': None,
                                'related_item': "DocumentField",
                                'error_text': None,
                                "related_info": None,
                                "secure_text": False,
                                "related_template": {
                                    "id": 1,
                                    "name": "Аниме_Акт_1",
                                    "type": "ACT",
                                    "template_file": "?????????????",
                                    "related_contractor_person": {
                                        "todo": "contractor_person_documentation"
                                    },
                                    "related_executor_person": {
                                        "todo": "executor_person_documentation"
                                    }
                                }
                            },
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
                description="Доступ запрещён",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Пользователю запрещён метод. Текст ошибки может отличаться.",
                        value={
                            "status": 403,
                            "details": "Текст ошибки"
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
# endregion
class TemplateDocumentFieldsListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentFieldSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        template_id = self.kwargs.get('tid')
        return DocumentField.objects.filter(related_template_id=template_id)
    
    def create(self, request, *args, **kwargs):
        data = json.loads(json.dumps(request.data["data"]))
        
        error = field_validate(data, "Executor")
        if error is not None:
            return Response(
                DetailAndStatsSerializer({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'details': f"Неправильный формат значения в поле `{error['field_id']}`."
                }).data,
                status=status.HTTP_400_BAD_REQUEST
            )

        required_fields = Field.objects.filter(related_item="DocumentField", is_custom=False, is_required=True)
        missing_fields = [field.name for field in required_fields if not find_dataValue(data, field.key_name)]

        if missing_fields:
            return Response(
                DetailAndStatsSerializer({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'details': f"Отсутствуют необходимые поля: {', '.join(missing_fields)}"
                }).data,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            template = Template.objects.get(id=self.kwargs.get('tid'))
        except Template.DoesNotExist:
            return Response(
                DetailAndStatsSerializer({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'details': f"Шаблон с TID={self.kwargs.get('tid')} не найден."
                }).data,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            doc_field = DocumentField.objects.create(
                id=f"{find_dataValue(data, 'key_name')}__Template__{str(Template.objects.filter(id=template).name).replace(' ', '_')}",
                name=find_dataValue(data, 'name'),
                key_name=find_dataValue(data, 'key_name'),
                is_required=find_dataValue(data, 'is_required'),
                type=find_dataValue(data, 'type'),
                validation_regex=find_dataValue(data, 'validation_regex'),
                related_item="Template",
                is_custom=True,
                related_info=None,
                placeholder=f"Введите значение поля {str(find_dataValue(data, 'name')).upper()}",
                related_template=Template.objects.filter(id=template), # Можно заменить на name но лучше не надо
            )

            return Response(ItemDetailsSerializer({
                "status": status.HTTP_201_CREATED,
                "details": DocumentFieldSerializer(doc_field).data,
            }).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                DetailAndStatsSerializer({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'details': f"Ошибка создания объекта модели `DocumentField`. {e}"
                }).data,
                status=status.HTTP_400_BAD_REQUEST
            )


# region TemplatesFields_docs
@extend_schema(tags=["Template"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список полей для создания объекта Template",
        responses={
            # Подробную документацию смотрите в TemplateListCreateView.GET.200.
            500: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
            )
        }
    )
)
# endregion
class TemplateFieldsView(generics.ListAPIView):
    queryset = Field.objects.filter(related_item="Template")
    serializer_class = FieldSerializer
    permission_classes = [permissions.AllowAny]


# region DocumentFields_docs
@extend_schema(tags=["Document"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список полей для создания объекта Document",
        responses={
            200: OpenApiResponse(
                response=DocumentFieldSerializer(many=True),
                description="Получен список полей для создания объекта `Document`",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Получен список полей для создания объекта `Document`. Поля могут быть разные в зависимости от выбранного шаблона документа. Для удобства показан только один элемент списка.",
                        value=[
                            {
                                'name': 'Название договора',
                                'key_name': '1__dogovor_name',
                                'is_required': True,
                                'placeholder': 'Название договора',
                                'type': 'TEXT',
                                'validation_regex': None,
                                'related_item': "DocumentField",
                                'error_text': None,
                                "related_info": None,
                                "secure_text": False,
                                "related_template": {
                                    "id": 1,
                                    "name": "Аниме_Акт_1",
                                    "type": "ACT",
                                    "template_file": "?????????????",
                                    "related_contractor_person": {
                                        "todo": "contractor_person_documentation"
                                    },
                                    "related_executor_person": {
                                        "todo": "executor_person_documentation"
                                    }
                                }
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
    )
)
# endregion
class DocumentFieldsView(generics.ListAPIView):
    # TODO: оказывается у нас нет методов для создания документа - надо бы это сделать.
    queryset = Field.objects.filter(related_item="Document")
    serializer_class = DocumentFieldSerializer
    permission_classes = [permissions.AllowAny]


# region TemplateOfCompany_docs
@extend_schema(tags=["Template"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список всех шаблонов (Templates) компании `company_id`",
        parameters=[
            OpenApiParameter(
                "company_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID компании",
                required=True,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=TemplateSerializer(many=True),
                description="Получен список всех шаблонов (Templates) компании `company_id`",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Получен список всех шаблонов (Templates) компании `company_id = 1`. Для удобства понимания структуры показан только один элемент списка.",
                        value=[
                            {
                                "id": 1,
                                "name": "Аниме_Акт_1",
                                "type": "ACT",
                                "template_file": "?????????????",
                                "related_contractor_person": {
                                    "todo": "contractor_person_documentation"
                                },
                                "related_executor_person": {
                                    "todo": "executor_person_documentation"
                                }
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
    )
)
# endregion
class TemplateCompanyListView(generics.ListAPIView):
    serializer_class = TemplateSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        return Template.objects.filter(related_executor_person__company=company_id)


# region TemplateCurrCompany_docs
@extend_schema(tags=["Template"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список всех шаблонов (Templates) компании, в которой зарегестрирован пользователь.",
        responses={
            200: OpenApiResponse(
                response=TemplateSerializer(many=True),
                description="Получен список всех шаблонов (Templates) компании, куда авторизирован пользователь.",
                examples=[
                    OpenApiExample(
                        "Пример ответа",
                        description="Получен список всех шаблонов (Templates) текущей компании. Для удобства понимания структуры показан только один элемент списка.",
                        value=[
                            {
                                "id": 1,
                                "name": "Аниме_Акт_1",
                                "type": "ACT",
                                "template_file": "?????????????",
                                "related_contractor_person": {
                                    "todo": "contractor_person_documentation"
                                },
                                "related_executor_person": {
                                    "todo": "executor_person_documentation"
                                }
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
                description="Ошибка на стороне сервера."
            )
        }
    )
)
# endregion
class TemplateCurrentCompanyListView(generics.ListAPIView):
    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Template.objects.filter(related_executor_person__company=self.request.user.company)


# template_detail(pk)

# TODO: Сделать тогда, когда будет сделан объект документа

@api_view(['GET'])
def document_list(request):
    documents = Document.objects.all()
    serializer = DocumentSerializer(documents, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def generate_document(request):
    if request.method == 'POST':
        # Необходимый шаблон будет как переменная
        pass