from rest_framework import serializers
from backend.models.company import Executor
from backend.models.user import Field

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Executor
        fields = ['id', 'company_name', 'company_fullName', 'created_at']

class CompanyFieldSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=Field.FIELD_TYPES)

    class Meta:
        model = Field
        fields = '__all__'