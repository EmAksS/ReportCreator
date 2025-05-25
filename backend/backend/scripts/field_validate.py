from backend.models.fields import Field
from backend.models.documents import DocumentField, TableField
import regex 
import json

FIELDS_DB = [
    Field,
    DocumentField, 
    TableField,
]

def field_validate(data: list[dict], type:str):
    """
    Принимает значения поля и проверяет их валидность через `validation_regex`.
    Возвращает ошибку если валидация провалена или None.
    """
    error = None

    print(data)

    for item in data:
        #print(item)
        field_id = item.get("field_id")
        value = item.get("value")

        if isinstance(value, list):
            for item in value:
                # Списки могут быть только для TableField
                error = field_validate(item, "TableField")
                if error is not None:
                    break
            return error

        print("value = ", value)
        
        for x in FIELDS_DB:
            field = x.objects.filter(key_name=field_id, related_item=type).first()
            if field is not None:
                break
        if field is None:
            error = {
                "field_id": field_id,
                "error": "Поле не было найдено в списке полей"
            }
            return error
        
        validation_regex = field.validation_regex
        if validation_regex is not None:
            re = regex.compile(validation_regex)
            if re.match(value) is None:
                error = {
                    "field_id": field_id,
                    "error": "Неверный формат по validation_regex"
                }
                break

    return error