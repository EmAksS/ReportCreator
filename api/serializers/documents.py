from rest_framework import serializers
from backend.models import documents
from backend.scripts.field_validate import field_validate

class TemplateSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=documents.Template.DOCUMENT_TYPES)
    
    class Meta:
        model = documents.Template
        fields = '__all__'

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