from django.db import models
from .documents import Document
from .fields import AbstractField
from .company import Executor

class Table(models.Model):
    """
    Модель информации о таблице
    """

    name = models.CharField(max_length=255)
    related_document = models.ForeignKey(Document, on_delete=models.CASCADE)
    company = models.ForeignKey(Executor, on_delete=models.CASCADE)

class TableField(AbstractField):
    related_table = models.ForeignKey(Table, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'related_table')

class TableValue(models.Model):
    table_field = models.ForeignKey(TableField, on_delete=models.CASCADE)
    row_number = models.IntegerField()
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('table_field', 'row_number')
