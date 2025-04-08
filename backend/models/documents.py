from django.db import models
from .company import ContractorPerson, ExecutorPerson
from .fields import AbstractField
import core.settings.base as core

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
    file = models.FileField(upload_to=core.BASE_DIR.parent/'docs/templates/', verbose_name="Файл шаблона")
    related_contractor_person = models.ForeignKey(ContractorPerson, on_delete=models.DO_NOTHING, verbose_name="Представитель (юридическое лицо) заказчика", null=True, blank=True)
    related_executor_person = models.ForeignKey(ExecutorPerson, on_delete=models.DO_NOTHING, verbose_name="Представитель (юридическое лицо) исполнителя", null=True, blank=True)
    
    def __str__(self):
        return self.name


class TemplateField(AbstractField):
    """
    Модель для хранение кастомных полей шаблона документов.
    """
    related_template = models.ForeignKey(Template, on_delete=models.DO_NOTHING, verbose_name="Связанный шаблон")


class Document(models.Model):
    """
        Абстрактная модель для всех документов в проекте.
        Все модели документов должны наследоваться от нее.

        Есть поля:
        - id - уникальный номер документа
        - created_at - дата создания документа
        - showDate - дата, которая отображается в документе (фактически, первая рабочая неделя месяца)
        - doc - путь к сохранённому документу
        - table - данные таблицы, если она там имеется с определёнными данными.
            check TODO
    """
    
    id = models.BigIntegerField(primary_key=True, verbose_name='Номер документа')
    template = models.ForeignKey(Template, on_delete=models.DO_NOTHING, verbose_name="Шаблон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    shown_date = models.DateField(verbose_name="Отображаемая дата")
    save_path = models.CharField(max_length=255, verbose_name="Путь к сохранённому документу относительно /docs/", null=True, blank=True)
    #TODO: table; Это будет ссылкой на другую модель базы данных, которая будет описана в `table.py`

class DocumentsValues(models.Model):
    """
    Вся информация касательно пользователей.
    """

    document_id = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='document_values'
    )
    field_id = models.ForeignKey(
        TemplateField,
        on_delete=models.CASCADE,
        related_name='document_field'
    )
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('document_id', 'field_id')

    def __str__(self):
        return f"{self.document_id} - {self.field_id}: {self.value}"