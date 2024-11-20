# Django проект собачьего приюта

## КАК УСТАНОВИТЬ И ЗАПУСТИТЬ СЕРВЕР

### Установка

1. Установить requirements
    ```shell
    pip3 install -r requirements.txt
    ```
2. Заполните .env file согласно файлу .env_sample
3. Создайте базу данных при помощи команды
   ```shell
   python manage.py ccdb
   ```
4. Примените миграции
   ```shell
   python manage.py migrate
   ```
5. Следующая команда создаст супер пользователя
   ```shell
   python manage.py ccsu
   ```
6. Используйте команду если хотите заполнить базу данных уже готовой фикстурой
   ```shell
   python manage.py loaddata data.json
   ```
### Запуск
1. Для начала запустите сервер [redis](https://skillbox.ru/media/base/kak_ustanovit_redis_v_os_windows_bez_ispolzovaniya_docker/) в отдельном powershell
   ```shell
   redis-server
   ```
2. После чего в ещё одном powershell с включенным виртуальным окружением и находясь в корневой папке запустите celery
   ```shell
   python manage.py runcelery
   ```
3. Теперь можно запустить сам сервер
   ```shell
   python manage.py runserver
   ```
   
## Информация

### Описание строк env файла

#### Database:
- MS_SQL_USER - Имя пользователя для входа
- MS_SQL_KEY - Пароль для входа
- MS_SQL_SERVER - Сервер
- MS_SQL_DATABASE - Название базы данных проекта (Придумать самому)
- MS_SQL_CREATED_DATABASE - Название любой уже созданной базы данных

#### Рассылка:
- MS_EMAIL_USER - Ваша gmail почта с которой будет происходить рассылка
- MS_EMAIL_PASSWORD - Пароль от почты или если есть 2-факторная аутентификация, то использовать [пароль приложения](https://support.google.com/accounts/answer/185833?hl=ru)

#### Cache:
- CACHE_ENABLED - Работа кеша (True или False)
- CACHE_LOCATION - Ссылка на redis сервер, нужен и для celery тоже (по стандарту ='redis://127.0.0.1:6379')