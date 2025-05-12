from rest_framework import serializers
from backend.models import User
from backend.models.user import UsersValues
from backend.models.fields import Field
from .company import CompanySerializer
from backend.scripts.field_validate import field_validate

class UserSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 
            'company', 'is_company_superuser',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

class UserFieldValueSerializer(serializers.ModelSerializer):
    # field = UserFieldSerializer(read_only=True)
    # field_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Field.objects.filter(related_item="User"),
    #     write_only=True,
    #     source='field'
    # )

    class Meta:
        model = UsersValues
        fields = '__all__'
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, data):
        # Проверяем, что поле принадлежит к типу "User"
        error = field_validate(data)
        if error is not None:
            return serializers.ValidationError(error, code=400)
        if data.get('field') and data['field'].related_item != "User":
            raise serializers.ValidationError(
                "Field должен относиться к User"
            )
        return data