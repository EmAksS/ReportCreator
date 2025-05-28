from rest_framework.response import Response
from rest_framework.views import APIView

class SchemaAPIView(APIView):
    """
    Базовый View, который добавляет общий формат ответа (success, message, details, errors).
    """
    details_serializer = None  # Сериализатор для поля `details`
    error_messages = None  # Словарь с возможными ошибками

    def finalize_response(self, request, response, *args, **kwargs):
        if isinstance(response, Response):
            data = response.data
            
            # Инициализируем wrapped_data с дефолтными значениями
            wrapped_data = {
                "details": None,
                "errors": None,
            }
            
            # Если data - словарь (обычный DRF-ответ)
            if isinstance(data, dict):
                if data.get("errors"):
                    wrapped_data["errors"] = data.pop("errors")
                wrapped_data["details"] = data if self.details_serializer else None
                
                # Сериализуем details если нужно
                if self.details_serializer and wrapped_data["details"]:
                    serializer = self.details_serializer(
                        wrapped_data["details"],
                        context=self.get_serializer_context(),
                    )
                    wrapped_data["details"] = serializer.data
            else:
                # Если data - не словарь (например, список)
                wrapped_data["details"] = data if self.details_serializer else None
                if self.details_serializer and wrapped_data["details"]:
                    serializer = self.details_serializer(
                        wrapped_data["details"],
                        context=self.get_serializer_context(),
                        many=isinstance(data, list)
                    )
                    wrapped_data["details"] = serializer.data
            
            response.data = wrapped_data
        return super().finalize_response(request, response, *args, **kwargs)