from rest_framework import serializers
from backend.models import documents
from backend.scripts.field_validate import field_validate
import os

class TemplateSerializer(serializers.ModelSerializer):
    #type = serializers.ChoiceField(choices=documents.Template.DOCUMENT_TYPES)
    
    class Meta:
        model = documents.Template
        fields = '__all__'

    def validate_file(self, value):
        """Проверка что файл является валидным DOCX"""
        # Проверка расширения
        ext = os.path.splitext(value.name)[1].lower()
        if ext != '.docx':
            raise serializers.ValidationError('Разрешены только файлы с расширением .docx')
        
        # Проверка сигнатуры DOCX (первые 4 байта)
        file_pos = value.tell()
        first_bytes = value.read(4)
        value.seek(file_pos)  # Возвращаем позицию
        
        if first_bytes != b'PK\x03\x04':
            raise serializers.ValidationError('Файл не является валидным DOCX документом')
        
        return value
    
    def to_internal_value(self, data):
        """
        Преобразуем входящий массив полей в словарь для сериализатора
        """
        # Если данные уже в правильном формате (например, при тестировании)
        if isinstance(data, dict) and 'file' in data:
            return super().to_internal_value(data)
        
        # Обрабатываем массив полей из фронтенда
        processed_data = {'template_file': None}
        
        for field in data:
            if field['field_id'] == 'template_file':
                processed_data['template_file'] = field['value']
            else:
                processed_data[field['field_id']] = field['value']
        
        return super().to_internal_value(processed_data)

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = documents.Document
        fields = '__all__'

class DocumentFieldSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=documents.DocumentField.FIELD_TYPES)

    class Meta:
        model = documents.DocumentField
        fields = '__all__'

class DocumentFieldValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = documents.DocumentsValues
        fields = '__all__'
    
    def validate(self, data):
        # Проверяем, что поле принадлежит к типу "Document"
        error = field_validate(data)
        if error is not None:
            return serializers.ValidationError(error, code=400)
        if data.get('field') and data['field'].related_item != "Document":
            raise serializers.ValidationError(
                "Field должен относиться к Document"
            )
        return data

class TableFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = documents.TableField
        fields = '__all__'

class TableFieldValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = documents.TableValues
        fields = '__all__'
