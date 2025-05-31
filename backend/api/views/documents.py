from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from api.views.schema import SchemaAPIView
from rest_framework.exceptions import ValidationError
# Permissions
from rest_framework import permissions
from api.permissions import IsAuthed, IsAuthedOrReadOnly
# models 
from backend.models.fields import Field
from backend.models.documents import Template, Document, DocumentField, TableField, DocumentsValues, TableValues
from backend.models.company import ContractorPerson, ExecutorPerson, Executor
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
    TableFieldSerializer,
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
from backend.scripts.fill_document import fill_document, find_fields
import json
from backend.scripts.find_datavalue import find_dataValue
from backend.scripts.load_data import load_data
# file settings
from django.conf import settings
import os
#from magic import Magic
from workalendar.europe import Russia
from datetime import date
from core.settings.base import DOCUMENTS_FOLDER, MEDIA_ROOT
import locale

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
        return Response({
            "details": [
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
            ],
            "errors": None
            }, status=status.HTTP_200_OK)


class FieldTypesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        from backend.models import fields
        types = fields.AbstractField.FIELD_TYPES
        
        ans = []

        for t in types:
            if t[0] == "FILE" or t[0] == "COMBOBOX":
                continue
            ans.append({
                "id": t[0],
                "name": t[1],
            })
        return Response({
            "details": ans,
            "errors": None
        }, status=status.HTTP_200_OK)



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
class TemplateListCreateView(SchemaAPIView, generics.ListCreateAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    details_serializer = TemplateSerializer
    permission_classes = [IsAuthedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, *args, **kwargs):
        self.details_serializer = FieldSerializer
        fields = Field.objects.filter(related_item="Template")
        return Response(FieldSerializer(fields, many=True).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = []

        # # Код ниже работает только для DRF-создания, но не через axios.
        # if 'template_file' in request.FILES:
        #     data.append({
        #         'field_id': 'template_file',
        #         'value': request.FILES['template_file']
        #     })

        # for key, value in request.data.items():
        #     if str(key).startswith('csrf'):
        #         continue
        #     data.append({
        #         'field_id': key,
        #         'value': value
        #     })

        # Ниже код только для axios.
        index = 0
        while True:
            field_id_key = f"{index}[fieldId]"
            value_key = f"{index}[value]"

            if field_id_key not in request.data:
                break
            field_id = request.data[field_id_key]

            if value_key in request.FILES:
                value = request.FILES[value_key]
            else:
                value = request.data.get(value_key)

            data.append({
                'field_id': field_id,
                'value': value
            })

            index += 1

        error = field_validate(data, "Template")
        if error is not None:
            raise ValidationError({error["field_id"]: error["error"]})

        try: 
            contractor = ContractorPerson.objects.get(id=find_dataValue(data, 'related_contractor_person'))
        except:
            return Response({"related_contractor_person": "Не найдено юридическое лицо заказчика"}, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            executor = ExecutorPerson.objects.get(id=find_dataValue(data, 'related_executor_person'))
        except:
            return Response({"related_contractor_person": "Не найдено юридическое лицо исполнителя"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # template = Template(
            #     name=find_dataValue(data, 'name'),
            #     type=find_dataValue(data, 'type'),
            #     file=file_path,
            #     related_contractor_person=contractor,
            #     related_executor_person=executor,
            # )
            serializer = self.serializer_class(data=data)
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                raise ValidationError({"template_name": "Данный шаблон уже существует."})
            return Response({"unknown": f"Неизвестная ошибка: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        self.details_serializer = TemplateSerializer

        if serializer.is_valid():
            serializer.save()
            # future_fields = find_fields(find_dataValue(data, "template_file"))
            # serializer.found_fields = future_fields
            return Response(self.details_serializer(serializer.instance).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateDetailDestroyView(SchemaAPIView, generics.RetrieveDestroyAPIView):
    serializer_class = TemplateSerializer
    details_serializer = TemplateSerializer
    permission_classes = [IsAuthedOrReadOnly]

    def get_queryset(self):
        tid = self.kwargs.get("pk", None)
        return Template.objects.get(id=tid)


class TemplateInfoView(SchemaAPIView, generics.GenericAPIView):
    serializer_class = TemplateSerializer
    details_serializer = TemplateSerializer
    permission_classes = [IsAuthedOrReadOnly]

    def get_queryset(self):
        tid = self.kwargs.get("tid", None)
        return Template.objects.filter(id=int(tid)).first()
    
    def get(self, request, *args, **kwargs):
        template = self.get_queryset()
        if template is None:
            return Response({"template": "Шаблон не найден"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.details_serializer(template).data, status=status.HTTP_200_OK)


# region DocumentFields_docs
@extend_schema(tags=["DocumentField"])
@extend_schema_view(
    get=extend_schema(
        summary="Получить список полей для создания поля документа с ID шаблона `TID`",
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
# endregion
class TemplateDocumentFieldsListCreateView(SchemaAPIView, generics.ListCreateAPIView):
    serializer_class = DocumentFieldSerializer
    details_serializer = DocumentFieldSerializer
    permission_classes = [IsAuthedOrReadOnly]

    def get_queryset(self):
        template_id = self.kwargs.get('tid')
        return DocumentField.objects.filter(related_template=template_id)
    
    def create(self, request, *args, **kwargs):
        data = load_data(request.data)
        
        error = field_validate(data, "DocumentField")
        if error is not None:
            raise ValidationError({error["field_id"]: error["error"]})

        required_fields = Field.objects.filter(related_item="DocumentField", is_custom=False, is_required=True)
        missing_fields = [field.name for field in required_fields if find_dataValue(data, field.key_name) is None]

        if missing_fields:
            raise ValidationError({field_id: "Не указано обязательное поле."} for field_id in missing_fields)

        try:
            template = Template.objects.get(id=self.kwargs.get('tid'))
        except Template.DoesNotExist:
            raise ValidationError({"template_id": f"Шаблон с TID {self.kwargs.get('tid')} не найден."})
        
        try:
            doc_field = DocumentField.objects.create(
                id=f"{find_dataValue(data, 'key_name')}__Template__{str(Template.objects.filter(id=template.id).first().template_name).replace(' ', '_')}",
                name=find_dataValue(data, 'name'),
                key_name=find_dataValue(data, 'key_name'),
                is_required=find_dataValue(data, 'is_required'),
                type=find_dataValue(data, 'type'),
                validation_regex=find_dataValue(data, 'validation_regex'),
                related_item="DocumentField",
                is_custom=True,
                related_info=None,
                placeholder=f"Введите значение поля {str(find_dataValue(data, 'name')).upper()}",
                related_template=Template.objects.filter(id=template.id).first(), # Можно заменить на name но лучше не надо
            )

            return Response(self.serializer_class(doc_field).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                raise ValidationError({"key_name": "Данное поле в документе уже существует."})
            raise ValidationError({"unknown": f"Ошибка создания поля документа: {e}"})


# Вернуть поля для создания DocumentField
class TemplateDocumentFieldsFieldsView(SchemaAPIView, generics.ListAPIView):
    serializer_class = FieldSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Field.objects.filter(related_item="DocumentField", is_custom=False)


# TableFieldsListCreateView
# Создать поле столбца таблицы
class TableFieldsListCreateView(SchemaAPIView, generics.ListCreateAPIView):
    serializer_class = TableFieldSerializer
    details_serializer = TableFieldSerializer
    permission_classes = [IsAuthedOrReadOnly]

    def get(self):
        fields = Field.objects.filter(related_item="TableField", is_custom=False)
        self.details_serializer = FieldSerializer
        return Response(FieldSerializer(fields, many=True).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        self.details_serializer = TableFieldSerializer
        data = load_data(request.data)

        error = field_validate(data, "TableField")
        if error is not None:
            raise ValidationError({error["field_id"]: error["error"]})

        required_fields = Field.objects.filter(related_item="TableField", is_custom=False, is_required=True)
        missing_fields = [field.name for field in required_fields if not find_dataValue(data, field.key_name)]

        if missing_fields:
            raise ValidationError({field_id: "Не указано обязательное поле."} for field_id in missing_fields)
        
        template_id = data.get('related_template')
        try:
            template = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            raise ValidationError({"template_id": f"Шаблон с TID {template_id} не найден."})
        
        try:
            table_field = TableField.objects.create(
                id=f"{find_dataValue(data, 'key_name')}__Template__{str(Template.objects.filter(id=template).first().name).replace(' ', '_')}",
                name=find_dataValue(data, 'name'),
                key_name=find_dataValue(data, 'key_name'),
                order= find_dataValue(data, 'order'),
                is_required=find_dataValue(data, 'is_required'),
                type=find_dataValue(data, 'type'),
                validation_regex=find_dataValue(data, 'validation_regex'),
                related_item="Template",
                is_custom=True,
                is_summable=find_dataValue(data, 'is_summable'),
                related_info=None,
                placeholder=f"Введите значение поля {str(find_dataValue(data, 'name')).upper()}",
                related_template=Template.objects.filter(id=template).first(), # Можно заменить на name но лучше не надо
            )

            return Response(self.serializer_class(table_field).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                raise ValidationError({"key_name": "В шаблоне уже существует данный столбец таблицы с таким же названием или порядком."})
            raise ValidationError({"unknown": f"Ошибка создания поля столбца таблицы: {e}"})


# Проверить список толбцов таблицы для шаблона TK
class TemplateTableFieldsListView(SchemaAPIView, generics.ListAPIView):
    serializer_class = TableFieldSerializer
    details_serializer = TableFieldSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        template_id = self.kwargs.get('tk')
        return TableField.objects.filter(related_template=template_id)


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
class TemplateFieldsView(SchemaAPIView, generics.ListAPIView):
    queryset = Field.objects.filter(related_item="Template")
    serializer_class = FieldSerializer
    details_serializer = FieldSerializer
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
    ),
    post=extend_schema(
        summary="Создать объект `Document`",
        #...
    )
)
# endregion
class DocumentFieldsCreateView(SchemaAPIView, generics.ListCreateAPIView):
    serializer_class = DocumentFieldSerializer
    details_serializer = DocumentFieldSerializer
    permission_classes = [IsAuthedOrReadOnly]

    def get_queryset(self):
        self.details_serializer = DocumentFieldSerializer
        tid = self.kwargs.get('tid')
        return DocumentField.objects.filter(related_template=Template.objects.filter(id=tid).first())
    
    def create(self, request, *args, **kwargs):
        data = load_data(request.data)

        error = field_validate(data, "DocumentField")
        if error is not None:
            raise ValidationError({error["field_id"]: error["error"]})

        listfields = [columns.get('field_id') for columns in data if isinstance(columns.get('value'), list)]
        
        # Проверка что шаблон документа есть
        tid = self.kwargs.get('tid')
        template = Template.objects.filter(id=tid).first()
        if not template:
            raise ValidationError({"template_id": "Шаблон документа не найден"})
        
        # Создаём документ
        try:
            doc = Document.objects.get_or_create(
                id=Document.objects.filter().count() + 1,
                template=template,
                shown_date=Russia().add_working_days(date(date.today().year, date.today().month, 1), 0),
                save_path=DOCUMENTS_FOLDER/template.template_file.name.split('/')[-1],
            )
        except Exception as e:
            raise ValidationError({"unknown": f"Ошибка создания документа: ({e})"})
        
        # Заполняем DocumentValues
        document_data = {}
        document_settings = {}

        for field in data:
            document_data[field.get('field_id')] = field.get("value")
            try:
                DocumentsValues.objects.get_or_create(
                    document_id=doc,
                    field_id=Field.objects.filter(id=field.get('field_id'), related_item="DocumentField").first(),
                    value=field.get("value", ""),
                )
            except Exception as e:
                doc.delete()   # Удаляем документ, если произошла ошибка
                raise ValidationError({"unknown": f"Ошибка распределении значении полей документа: {e}"})
        
        ## Дополняем также информацией о компаниях
        locale.setlocale(locale.LC_ALL, 'ru_RU')
        # Информация о документе
        document_data["contract_number"] = template.related_contractor_person.company.contract_number
        document_data["contract_date"] = template.related_contractor_person.company.contract_date.strftime("%d.%m.%Y")
        #* order_date - в fill_document
        document_data["order_number"] = Document.objects.filter(related_template=template).count() + 1
        # Лицо заказчика
        if template.related_contractor_person is not None:
            document_data["contractor_person"] = template.related_contractor_person.set_initials()
            document_data["contractor_post"] = template.related_contractor_person.post if template.related_contractor_person.post else "Ответственное лицо"
            document_data["contractor_company_full"] = template.related_contractor_person.company.company_fullName
            document_data["contractor_company"] = template.related_contractor_person.company.company_name
        # Лицо исполнителя
        if template.related_executor_person is not None:
            document_data["executor_person"] = template.related_executor_person.set_initials()
            document_data["executor_post"] = template.related_executor_person.post if template.related_executor_person.post else "Ответственное лицо"
            document_data["executor_company_full"] = template.related_executor_person.company.company_fullName
            document_data["executor_company"] = template.related_executor_person.company.company_name


        # Делаем так, чтобы столбцы таблицы располагались по возрастанию ORDER
        ordered_lf = []
        ordered = TableField.objects.filter(related_template=tid).order_by('order')
        for row in ordered:
            if row.key_name not in listfields:
                continue
            ordered_lf.append(row.key_name)

        if TableField.objects.filter(related_template=tid, is_summable=True).count() > 1:
            raise ValidationError({"unknown": "В таблице может быть только один суммируемый столбец"})
        summable_index = ordered_lf.index(TableField.objects.filter(related_template=tid, is_summable=True).first().key_name) if TableField.objects.filter(related_template=tid, is_summable=True).exists() else None
        
        maxlen = 0
        for listfield in ordered_lf:
            maxlen = max(maxlen, len(find_dataValue(data, listfield)))
        
        table = []
        for row in range(len(maxlen)):
            rowlist = []
            for listfield in ordered_lf:
                try:
                    rowlist.append(find_dataValue(data, listfield)[row])
                except:
                    rowlist.append("")
            table.append(rowlist)

        if summable_index is not None:
            document_data["total_cost"] = round(sum([0 if rowlist[summable_index] == "" else float(rowlist[summable_index]) for rowlist in table]), 2)
            document_settings["summable_type"] = TableField.objects.filter(related_template=tid, is_summable=True).first().type

        # Создаём сам документ.
        try:
            info = fill_document(template.template_file.name, document_data, table, document_settings)
            if info.get("error"):
                raise ValidationError({"unknown": f"Ошибка создания документа: ({info['error']})"})
            doc.shown_date = info.get("shown_date")
            if info.get("path"):
                doc.save_path = info["path"]
        except Exception as e:
            doc.delete()   # Удаляем документ, если произошла ошибка
            raise ValidationError({"unknown": f"Ошибка создания документа: ({e}). Информация: {info}"})

        #print(info)
        self.details_serializer = DocumentSerializer
        return Response(DocumentSerializer(doc).data, status=status.HTTP_201_CREATED)


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
class TemplateCompanyListView(SchemaAPIView, generics.ListAPIView):
    serializer_class = TemplateSerializer
    details_serializer = TemplateSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        company = Executor.objects.filter(id=company_id).first()
        return Template.objects.filter(related_executor_person__company=company)


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
class TemplateCurrentCompanyListView(SchemaAPIView, generics.ListAPIView):
    serializer_class = TemplateSerializer
    details_serializer = TemplateSerializer
    permission_classes = [IsAuthed]

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