def find_dataValue(data: list[dict], name: str):
    """
        В словаре data возвращает `value` для `field_id` = `name`.
        Если такого поля нет возвращает `None`.

        Прим. поиск выполняется при формате data:
        ```
        [
            {
                "field_id": "name",
                "value": "returning_this"
            },
            //...
        ]
        ```
    """
    for item in data:
        if item.get("field_id") == name:
            return item.get("value")
    return None