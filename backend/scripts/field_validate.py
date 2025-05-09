from backend.models.fields import Field
import regex 
import json

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

        print("value = ", value)
        
        field = Field.objects.get(key_name=field_id, related_item=type)
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