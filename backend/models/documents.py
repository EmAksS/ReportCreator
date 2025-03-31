from django.db import models
from .company import Executor, Contractor


from django.db import models

class Template(models.Model):
    """
    Модель для хранения шаблонов документов.
    """
    DOCUMENT_TYPES = [
        ('ACT', 'Акт'),
        ('ORDER', 'Заказ'),
        ('REPORT', 'Отчёт'),
    ]

    DATA_TYPES = [
        ('text', 'Текст'),
        ('number', 'Число'),
        ('date', 'Дата'),
        ('money', 'Денежная сумма'),
        ('person', 'Личность'),
    ]

    name = models.CharField(max_length=255, verbose_name="Название шаблона")
    type = models.CharField(max_length=10, choices=DOCUMENT_TYPES, verbose_name="Тип документа")
    file = models.FileField(upload_to='docs/templates/', verbose_name="Файл шаблона")
    custom = models.JSONField(default=dict, verbose_name="Дополнительные переменные") # Пока не работает но хз
    related_company = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="Связанная компания")

    def __str__(self):
        return self.name


class Document(models.Model):
    """
        Абстрактная модель для всех документов в проекте.
        Все модели документов должны наследоваться от нее.

        Есть поля:
        - id - уникальный номер документа
        - contrator - компания-заказчик
        - executor - компания-исполнитель
        - created_at - дата создания документа
        - showDate - дата, которая отображается в документе (фактически, первая рабочая неделя месяца)
        - doc - файл с документом-шаблоном для изменения
        - table - данные таблицы, если она там имеется с определёнными данными.
            Задаётся в формате `list` по типу [{'поле1': 'значение1', 'поле2': 'значение2'}, ...]
        - custom - дополнительные данные, которые вставляются в документ (задаются пользователем).
            Задаётся в формате `dict` по типу {'поле1__тип-данных': 'значение1', 'поле2__тип-данных': 'значение2'}
    """
    
    id = models.BigIntegerField(primary_key=True, verbose_name='Номер документа')
    template = models.ForeignKey(Template, on_delete=models.DO_NOTHING, verbose_name="Шаблон")
    contrator = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING, verbose_name="Заказчик")
    executor = models.ForeignKey(Executor, on_delete=models.DO_NOTHING, verbose_name="Исполнитель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    showDate = models.DateField(verbose_name="Отображаемая дата")
    table = models.JSONField(default=list)
    custom = models.JSONField(default=dict)