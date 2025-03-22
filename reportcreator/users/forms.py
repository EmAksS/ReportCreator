"""
Форма аутентификации пользователя в систему.
У модели пользователя, как объекта аутентификации в систему, имеются следующие поля:
- `username` - имя пользователя, под которм он входит в систему. 
Должно быть уникальным в рамках всей системы.
Максимальная длина имени - 150 символов.
Может содержать цифры, буквы, символы "@", ".", "+", "-" и "_".
Является ключевым полем для связи с `models.User`.
- `email` - адрес электронной почты, к которому будет привязан пользователь.
Соостветствие правильности происходит с помощью средств Django (`models.EmailField`).
- `password` - пароль пользователя.
Максимальная длина пароля - 128 символов.

Все данные о пользователях сохраняются в базе данных `auth_user`?
"""
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms
from companies import models as companies

class SignUpForm(UserCreationForm):
    last_name = forms.CharField(max_length=63, help_text='Введите вашу фамилию.')
    first_name = forms.CharField(max_length=63, help_text='Введите ваше имя.')
    patronymic = forms.CharField(max_length=63, required=False, help_text='Введите ваше отчество (если имеется).')
    related_company = forms.ModelChoiceField(queryset=companies.Executor.objects.all(), help_text='Выберите вашу компанию. Если не уверены в вашей компании - оставьте поле пустым и обратитесь к Администратору.')
    
    # TODO: Написать проверку пароля так, чтобы он проверялся через регулярное выражение
    class Meta:
        model = CustomUser
        fields = ('username', 'last_name', 'first_name', 'patronymic', 'related_company', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)