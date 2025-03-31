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
    - Название должности, от имени которого осуществляется подпись документа
    - ФИО должности, от чьего имени осуществляется подпись документа
    - Инициалы ФИО руководителя компании. TODO: сделать его автовычислимым согласно скрипту (ФАМИЛИЯ И. О.)
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
    contractor_city = models.CharField(max_length=64, null=False)