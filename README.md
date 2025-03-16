# Telegram Contact Bot

Простой Telegram-бот для сбора контактов пользователей и сохранения их в базу данных SQLite.

## Функциональность

- Запрашивает контакт пользователя через кнопку "Поделиться контактом"
- Сохраняет имя, никнейм и телефон пользователя в базу данных SQLite
- Отправляет подтверждение о сохранении контакта

## Установка и запуск

### Локальная разработка

1. Клонировать репозиторий:
```bash
git clone https://github.com/yourusername/contact-bot.git
cd contact-bot
```

2. Создать виртуальное окружение и установить зависимости:
```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux/macOS
# или
venv\Scripts\activate  # Для Windows
pip install -r requirements.txt
```

3. Запустить бота:
```bash
python Contact-bot.py
```

### Установка на сервере

1. Клонировать репозиторий на сервер:
```bash
git clone https://github.com/yourusername/contact-bot.git
cd contact-bot
```

2. Установить зависимости:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Запустить бота в фоновом режиме:
```bash
# Установить screen, если его нет
apt install screen -y

# Создать новую screen-сессию
screen -S contactbot

# Запустить бота
python Contact-bot.py

# Отсоединиться от сессии (Ctrl+A, затем D)
```

## Структура базы данных

Бот создает базу данных SQLite `contacts.db` со следующей структурой:

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    first_name TEXT,
    username TEXT,
    phone_number TEXT,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Зависимости

- Python 3.7+
- aiogram 3.x
- SQLite3 (встроен в Python)