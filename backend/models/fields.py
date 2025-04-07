from django.db import models

class Field(models.Model):
    FIELD_TYPES = [
        ("TEXT", "Текстовое поле"),
        ("PASSWORD", "Пароль"),
        ("NUMBER", "Числовое поле"),
        ("DATE", "Дата и время"),
        ("CURRENCY", "Денежная сумма"),
        ("BOOL", "Логическое поле"),
        ("USER", "ФИО другого участника"),
    ]
        

    name = models.CharField(max_length=50, verbose_name='Русское название поля (для отображения)')
    englName = models.CharField(max_length=50, verbose_name='Английское название поля (по которому будет доступ в API)', primary_key=True)
    is_required = models.BooleanField(default=False, verbose_name='Обязательное поле?')
    relatedItem = models.CharField(max_length=30, editable=False, verbose_name='К какому виду записи относится это поле (заполняется программно)')
    type = models.CharField(max_length=10, verbose_name='Тип поля', choices=FIELD_TYPES)
    placeholder = models.CharField(max_length=50, null=True, verbose_name='Подсказка для заполнения поля')
    checkRegex = models.CharField(max_length=200, null=True, verbose_name='Регулярное выражение для валидации')

    def __str__(self):
        return self.englName