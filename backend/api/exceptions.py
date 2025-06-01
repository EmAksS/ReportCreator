from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from api.serializers.schema import StatusSerializer

def custom_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        serializer = StatusSerializer(data={
            "status": 401,
        })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=401)
    
    # Стандартная обработка остальных ошибок
    return exception_handler(exc, context)