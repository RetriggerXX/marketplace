# Инструкция для запуска проекта
## 1. Клонирование репозитория

### Откройте терминал и выполните команду:
git clone <URL_репозитория>

## 2. Создание файла .env

### Перейдите в папку: marketplace\src\core\ и создайте файл с именем .env

## 3. Настройка переменных окружения

### Откройте .env и пропишите следующие значения:


DEBUG=True  
SECRET_KEY='example_сode'  # Замените на свой секретный ключ  


NAME="postgres"            # Имя вашей базы данных  
USER="example_user"        # Пользователь базы данных  
PASS="example_pass"        # Пароль пользователя  
HOST="localhost"           # Хост базы данных  
PORT="5432"                # Порт базы данных  

EMAIL_PORT=587   
EMAIL_USE_TLS=True  
EMAIL_HOST_USER='example@example.com'       # Ваш email для рассылки кодов   
EMAIL_HOST_PASSWORD='example_password'     # Пароль от почты  
DEFAULT_FROM_EMAIL=EMAIL_HOST_USER

## 4. Запуск

### Пропишите в терминал команду:
docker-compose up --build

## 5. Проверка работы проекта

### Запустите адрес сайта:

#### http://localhost:8000/


