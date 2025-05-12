from rest_framework import serializers
# models
from backend.models.fields import Field

class FieldSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=Field.FIELD_TYPES)

    class Meta:
        model = Field
        fields = '__all__'