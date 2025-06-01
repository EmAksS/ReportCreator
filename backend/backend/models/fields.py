from django.db import models

class AbstractField(models.Model):
    FIELD_TYPES = [
        ("TEXT", "Текстовое поле"),
        ("NUMBER", "Числовое поле"),
        ("DATE", "Дата и время"),
        ("CURRENCY", "Денежная сумма"),
        ("BOOL", "Логическое поле"),
        ("USER", "ФИО другого участника"),
        #("FILE", "Файл"),
        ("COMBOBOX", "Выпадающий список из других записей")
    ]
    
    id = models.CharField(primary_key=True, max_length=128)
    name = models.TextField(max_length=50, verbose_name='Русское название поля (для отображения)')
    key_name = models.CharField(max_length=50, verbose_name='Английское название поля (по которому будет доступ в API)')
    is_required = models.BooleanField(default=False, verbose_name='Обязательное поле?')
    related_item = models.CharField(max_length=30, editable=False, verbose_name='К какому виду записи относится это поле (заполняется программно)')
    type = models.CharField(max_length=10, verbose_name='Тип поля', choices=FIELD_TYPES)
    related_info = models.JSONField(null=True, editable=False, verbose_name='Дополнительная информация для этого поля при related_item = COMBOBOX')
    placeholder = models.CharField(max_length=50, null=True, verbose_name='Подсказка для заполнения поля')
    validation_regex = models.CharField(max_length=200, null=True, verbose_name='Регулярное выражение для валидации')
    secure_text = models.BooleanField(default=False, verbose_name='Это защищённое поле?')
    error_text = models.TextField(null=True, verbose_name='Текст ошибки при валидации')
    is_custom = models.BooleanField(default=False, editable=False, verbose_name='Это поле создано пользователем?')

    def __str__(self):
        return self.key_name

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['key_name', 'related_item'], name='abstract_key_name_related_item_combination'
            )
        ]

class Field(AbstractField):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['key_name', 'related_item'], name='field_key_name_related_item_combination'
            )
        ]