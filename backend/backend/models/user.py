from django.db import models
from django.contrib.auth.models import AbstractUser
from .company import Executor
from .fields import *

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
    username = models.CharField(max_length=150, primary_key=True, null=False)
    company = models.ForeignKey(Executor, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    is_company_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class UsersValues(models.Model):
    """
    Вся информация касательно пользователей.
    """

    id = models.CharField(max_length=150, primary_key=True, unique=True)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_values'
    )
    field_id = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        related_name='user_field'
    )
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['key_name', 'related_item'], name='abstract_key_name_related_item_combination'
        #     )
        # ]
        pass

    def __str__(self):
        return f"{self.user_id} - {self.field_id}: {self.value}"