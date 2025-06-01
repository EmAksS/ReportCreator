from rest_framework import serializers

class FieldValueSerializer(serializers.Serializer):
    field_id = serializers.CharField(help_text="`key_name` поля из таблицы Field или его наследников")
    value = serializers.CharField(help_text="Значение поля")

class DataInputSerializer(serializers.Serializer):
    data = serializers.ListField(
        child=FieldValueSerializer(),
        help_text="Список объектов {field_id, value}"
    )

class StatusSerializer(serializers.Serializer):
    status = serializers.IntegerField()

class DetailAndStatsSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    details = serializers.CharField()

class ItemDetailsSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    details = serializers.DictField()