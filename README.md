# Приложение «Продуктовый помощник» 
## Функционал:
- Позволяет публиковать рецепты
- Добавлять рецепты в избранное
- Подписываться на публикации других авторов
- Сервис "Список покупок", позволяет создавать список продуктов, который потом можно скачать
- Интерфейс администратора

## Подготовка рабочей среды
Перейдите в свою рабочую директорию и выполните следующие команды:
```
git clone https://github.com/avcherezov/foodgram-project
cd foodgram-project
```
Создайте в корне проекта файл .env со следующими данными:
```
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
Выполните команду:
```
docker-compose up --build -d
```
Выполните миграции:
```
docker-compose exec web python manage.py migrate
```
Создайте суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
Запустите сервер разработки:
```
docker-compose exec web python manage.py runserver
```

## Стэк
Django, Gunicorn, Nginx, PostgreSQL, Docker, Яндекс.Облако

## Адрес проекта в сети
http://84.201.166.209/
