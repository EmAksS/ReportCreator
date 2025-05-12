# rest
from rest_framework import generics, status
# Permissions
from rest_framework.permissions import AllowAny
# Response
from rest_framework import status
# serializers
from api.serializers.field import FieldSerializer
# models
from backend.models.fields import Field
# autodocs
from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
    OpenApiResponse,
)

@extend_schema(tags=['Field'])
@extend_schema_view(
    get=extend_schema(
        summary="Получить поля для создания нового поля Field",
        responses={
            status.HTTP_200_OK: FieldSerializer(many=True),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                response=None,
                description="Ошибка на стороне сервера"
                ),
        }
    )
)
class FieldFieldsListView(generics.ListAPIView):
    queryset = Field.objects.filter(related_item="Field", is_custom=False)
    serializer_class = FieldSerializer
    permission_classes = [AllowAny]