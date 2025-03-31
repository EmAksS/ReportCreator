from rest_framework import serializers
from backend.models.company import Executor

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Executor
        fields = ['id', 'company_name', 'company_fullName', 'created_at']