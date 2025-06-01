from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import random

class CompanyAbstract(models.Model):
    """
    Базовая абстрактная модель компании, от которой будут наследоваться другие модели.

    Здесь определены базовые поля, которые имеются как в Исполнителе, так и в 
    Заказчике, такие как:
    - Уникальный идентификационный номер компании (создаётся автоматически)
    - Название компании
    - Полное название компании с расшифровкой всех абревиатур
    """
    class Meta:
        abstract = True
    
    company_name = models.CharField(max_length=64)
    company_fullName = models.CharField(max_length=256, null=False, default=company_name)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class Executor(CompanyAbstract):
    """
    Модель компании исполнителя. 
    Наследует все поля из Company.

    TODO: Добавляет ли он дополнительные поля?
    """

class Contractor(CompanyAbstract):
    """
    Модель компани-заказчика.
    Наследует все поля из Company, а также добавляет:
    - Город-месторасположение компании, где происходит подпись документа.
    """
    related_executor = models.ForeignKey(Executor, on_delete=models.CASCADE, related_name='related_executor', default=0)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['company_name', 'company_fullName', 'related_executor'], name='company_names_combination'
            )
        ]

class Person(models.Model):
    """
    Модель юридического лица.
    Является абстрактной моделью, от которой будут наследоваться модели
    юрлица-заказчика и юрлица-исполнителя.
    НЕ ЯВЛЯЮТСЯ ПОЛЬЗОВАТЕЛЯМИ СИСТЕМЫ!
    Они являются больше абстраткными обёртками, от имени которых будут подписываться документы.
    - ФИО лица
    - Должность лица
    """

    class Meta:
        abstract = True

    person_type = models.TextField(max_length=128, null=False, default="OAO 'Название компании'") # OAO "Название компании"
    first_name = models.CharField(max_length=64, null=False)
    last_name = models.CharField(max_length=64, null=False)
    surname = models.CharField(max_length=64, null=False)
    post = models.CharField(max_length=64, null=False)

    def set_initials(self):
        return f'{self.last_name} {self.first_name[0]}.{self.surname[0]}.'

class ExecutorPerson(Person):
    """
    Модель юридического лица-исполнителя.
    Наследует все поля из Person.
    - Компания-исполнитель, которой принадлежит лицо
    """
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['first_name', 'last_name', 'surname', 'company'], name='FIO_executor_combination'
            )
        ]

    company = models.ForeignKey(Executor, on_delete=models.CASCADE)

class ContractorPerson(Person):
    """
    Модель юридического лица-заказчика.
    Наследует все поля из Person.
    """
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['first_name', 'last_name', 'surname', 'company'], name='FIO_contractor_combination'
            )
        ]

    contractor_city = models.CharField(max_length=64, null=False)
    contract_number = models.IntegerField(null=False) # Номер договора
    contract_date = models.DateTimeField(auto_now_add=False)
    company = models.ForeignKey(Contractor, on_delete=models.CASCADE)