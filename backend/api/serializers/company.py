from rest_framework import serializers
from backend.models.company import Executor, Contractor, ExecutorPerson, ContractorPerson
from backend.models.user import Field

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Executor
        fields = '__all__'

class CompanyExecutorPersonSerializer(serializers.ModelSerializer):
    initials = serializers.CharField(source='set_initials', read_only=True)
    
    class Meta:
        model = ExecutorPerson
        fields = '__all__'

class CompanyContractorPersonSerializer(serializers.ModelSerializer):
    initials = serializers.CharField(source='set_initials', read_only=True)
    
    class Meta:
        model = ContractorPerson
        fields = '__all__'

class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = '__all__'

