from rest_framework.response import Response
from rest_framework.views import APIView

class SchemaAPIView(APIView):
    """
    Универсальный View с правильной обработкой:
    - GET (один объект)
    - GET (список)
    - POST/PUT/PATCH (успех)
    - Ошибки валидации
    """
    details_serializer_class = None  # Переименовано для ясности
    error_messages = None

    def finalize_response(self, request, response, *args, **kwargs):
        if not isinstance(response, Response):
            return super().finalize_response(request, response, *args, **kwargs)

        original_data = response.data
        result = {
            "details": None,
            "errors": None
        }

        # Обработка ошибок валидации (status_code 4XX)
        if 400 <= response.status_code < 500:
            result["errors"] = original_data
            response.data = result
            return super().finalize_response(request, response, *args, **kwargs)

        # Обработка успешных ответов
        if self.details_serializer_class:
            # Для списков
            if isinstance(original_data, list):
                serializer = self.details_serializer_class(
                    original_data,
                    many=True,
                    context=self.get_serializer_context()
                )
                result["details"] = serializer.data
            
            # Для одного объекта
            elif isinstance(original_data, dict):
                # Проверяем, есть ли в данных поля сериализатора
                serializer = self.details_serializer_class(
                    data=original_data,
                    context=self.get_serializer_context()
                )
                if serializer.is_valid(raise_exception=False):
                    result["details"] = serializer.validated_data
                else:
                    result["details"] = original_data
            
            # Для QuerySet или других итерируемых объектов
            else:
                try:
                    serializer = self.details_serializer_class(
                        original_data,
                        many=hasattr(original_data, '__iter__') and not isinstance(original_data, (dict, str)),
                        context=self.get_serializer_context()
                    )
                    result["details"] = serializer.data
                except Exception:
                    result["details"] = original_data
        else:
            result["details"] = original_data

        response.data = result
        return super().finalize_response(request, response, *args, **kwargs)