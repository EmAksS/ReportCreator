from django.db import models
from django.contrib.auth.models import AbstractUser
from .company import Executor

class User(AbstractUser):
    """
    Модель пользователя системы, который выполняет работу с системой.
    Каждый пользователь связан с конкретной компанией-исполнителем.
    Пользователь может быть связан только с одной конкретной компанией.

    Здесь представлена только информация с пользователем, как объектом системы.
    Чтобы получить информацию о пользователе, как объекта для аутентификации, смотрите `forms.py`.

    Поля пользователя:
    username - имя пользователя в системе.
    last_name - фамилия пользователя.
    first_name - имя пользователя.
    patronymic - отчество пользователя.
    related_company - компания, которой принадлежит пользователь. Является полем таблицы `companies.Executor`.
    """
    username = models.CharField(max_length=150, unique=True, null=False)
    last_name = models.CharField(max_length=63, null=False)
    first_name = models.CharField(max_length=63, null=False)
    patronymic = models.CharField(max_length=63, null=True)
    company = models.ForeignKey(Executor, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    is_company_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username