# Запуск программы на своей машине

### 1. Скачать и установить код в папке по своему усмотрению

С помощью git clone или через архив

### 2. Скачать и установить СУБД PostgreSQL

### 3. Скачать и установить Docker

### 4. Создать образ и запустить контейнер в корне папки

Главный контейнер запускается командой\
$ docker compose up -d

Работает на порте 8000.

Тестовый контейнер запускается командой\
$ docker compose -f docker-compose-test.yaml -p test up -d

Работает на порте 8001. Тесты запускаются командой\
$ pytest

Вывод количества подменю и блюд для Меню через один (сложный) ORM запрос находится в src/routers/menu.py на строках 21 и 49.
