<h1 align="center">Ситсема формирования отчетов <b>WReport</b></h1>
<h3>Здеcь будут содержать все файлы для командного проекта по формирования отчетов компании между заказчиками</h3>

# Клонирование репозитория
1. Выполните клонирование репозитория через команду в нужную директорию:
```
git clone https://github.com/EmAksS/ReportCreator.git
```
2. Создадите и запустите виртуальную среду в директории `reportcreator`:
```
python -m venv venv
.\venv\Scripts\activate
```
3. Установите все зависимости через `requirements.txt`
```
pip install -r ../requirements.txt
```
4. Создадите и заполните `.env`-файл. Структура переменных описана в файле `.env.dist`
    - Значение `DEBUG` ставить на `True`, кроме случаев загрузки сайта на продакшн.
    - Значение `SECRET_KEY` лучше получить, создав пустой проект Django и взяв оттуда значение SECRET_KEY:
    ```
    django-admin startproject testtest
    ```
    После чего в файле `testtest\testtest\settings.py` находим поле `SECRET_KEY`.
4. Создайте новую ветку Git'a для работы.

# Запуск приложения
1. Перейдите в директорию `reportcreator`.
2. Введите команду:
```
python manage.py runserver
```
3. Перейдите по ссылке http://127.0.0.1:8000/ в браузере.

*Все другие вопросы спрашивайте на странице проекта в Трекере.*