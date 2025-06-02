from django.db import models
from .company import ContractorPerson, ExecutorPerson
from .fields import AbstractField
from core.settings.base import TEMPLATES_FOLDER, DOCUMENTS_FOLDER

class Template(models.Model):
    """
    Модель для хранения шаблонов документов.
    """
    DOCUMENT_TYPES = [
        ('ACT', 'Акт'),
        ('ORDER', 'Заказ'),
        ('REPORT', 'Отчёт'),
    ]

    template_name = models.CharField(max_length=255, verbose_name="Название шаблона")
    template_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES, verbose_name="Тип документа")
    template_file = models.FileField(upload_to='templates/', verbose_name="Файл шаблона", null=True, blank=True)
    related_contractor_person = models.ForeignKey(ContractorPerson, on_delete=models.CASCADE, verbose_name="Представитель (юридическое лицо) заказчика", null=True, blank=True)
    related_executor_person = models.ForeignKey(ExecutorPerson, on_delete=models.CASCADE, verbose_name="Представитель (юридическое лицо) исполнителя", null=True, blank=True)
    
    def __str__(self):
        return self.template_name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['related_contractor_person', 'related_executor_person', 'template_name'], name='persons_name_combination'
            )
        ]


class DocumentField(AbstractField):
    """
    Модель для хранение кастомных полей шаблона документов.
    """
    related_template = models.ForeignKey(Template, on_delete=models.CASCADE, verbose_name="Связанный шаблон")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['key_name', 'related_item', 'related_template'], name='document_field_key_name_related_item_combination'
            )
        ]


class TableField(AbstractField):
    """
    Модель для хранения данных формата столбцов таблицы в документе.
    """
    #shown_header = models.CharField(max_length=255, verbose_name="Заголовок столбца")
    order = models.IntegerField(verbose_name="Порядок столбца")
    is_summable = models.BooleanField(default=False, verbose_name="Суммируемый столбец")
    is_autoincremental = models.BooleanField(default=False, verbose_name="Автосуммируемый столбец")
    related_template = models.ForeignKey(Template, on_delete=models.CASCADE, verbose_name="Связанный шаблон")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['key_name', 'related_item', 'related_template'], name='table_field_key_name_related_item_combination'
            ),
            models.UniqueConstraint(
                fields=['order', 'related_template'], name='table_field_order_related_item_combination'
            )
        ]


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
    template = models.ForeignKey(Template, on_delete=models.CASCADE, verbose_name="Шаблон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    shown_date = models.DateField(verbose_name="Отображаемая дата")
    save_path = models.CharField(max_length=255, verbose_name=f"Путь к сохранённому документу относительно {DOCUMENTS_FOLDER}", null=True, blank=True)
    document_number = models.IntegerField(verbose_name="Номер документа в шаблоне", default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.document_number = Document.objects.filter(
                template__related_contractor_person=self.template.related_contractor_person,
                template__related_executor_person=self.template.related_executor_person,
                template__template_type=self.template.template_type
                ).count() + 1
        super().save(*args, **kwargs)
        #return documents.Document.objects.filter(template=obj.template).count() + 1


class DocumentsValues(models.Model):
    """
    Вся информация касательно полей документа.
    """

    document_id = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='document_id'
    )
    field_id = models.ForeignKey(
        DocumentField,
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


class TableValues(models.Model):
    """
    Вся информация касательно значений полей таблицы.
    """

    row_number = models.IntegerField(verbose_name='Номер строки таблицы', default=0)
    document_id = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='document_id_table'
    )
    table_id = models.ForeignKey(
        TableField,
        on_delete=models.CASCADE,
        related_name='table_field'
    )
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('row_number', 'document_id', 'table_id')

    def __str__(self):
        return f"{self.document_id} - {self.table_id}[{self.row_number}]: {self.value}"
    
    def save(self, *args, **kwargs):
        # Autoincremental row_number
        if not self.order_number:
            last_entry = TableValues.objects.order_by('row_number').last()
            self.order_number = (last_entry.order_number + 1) if last_entry else 0
        super().save(*args, **kwargs)
