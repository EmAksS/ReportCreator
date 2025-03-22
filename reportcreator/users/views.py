from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from .models import CustomUser
from companies.models import Executor

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()          # Сохраняем нового пользователя
            login(request, user)        # Выполняем вход
            return redirect('login')     # Перенаправляем на главную страницу
    else:
        form = SignUpForm()
    # TODO: нельзя проверить ЭТО, потому что нужен signup.html
    return render(request, 'register.html', {'form': form})

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password) # Проверяем учетные данные
            if user is not None:
                login(request, user)     # Выполняем вход
                return redirect('/')  # Перенаправляем на главную страницу
    # TODO: нельзя проверить ЭТО, потому что нужен login.html
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')