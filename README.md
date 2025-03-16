# Telegram Bots Collection

Коллекция Telegram-ботов для различных целей.

## 1. Contact Bot

Простой Telegram-бот для сбора контактов пользователей и сохранения их в базу данных SQLite.

### Функциональность

- Запрашивает контакт пользователя через кнопку "Поделиться контактом"
- Сохраняет имя, никнейм и телефон пользователя в базу данных SQLite
- Отправляет подтверждение о сохранении контакта

### Структура базы данных

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

## 2. Scam Bot

Простой Telegram-бот для троллинга, который отвечает на сообщения пользователей.

### Функциональность

- На сообщение "да" (в любом регистре) отвечает "Так и знал"
- На все остальные сообщения отвечает "Сосал?"
- Имеет обработку ошибок и автоматический перезапуск при сбоях

## Установка и запуск

### Настройка переменных окружения

1. Создайте файл `.env` в корне проекта на основе `.env.example`:
```bash
cp .env.example .env
```

2. Откройте файл `.env` и добавьте ваш токен Telegram бота:
```
API_TOKEN=your_telegram_bot_token_here
```

Получить токен можно у [@BotFather](https://t.me/BotFather) в Telegram.

### Локальная разработка

1. Клонировать репозиторий:
```bash
git clone https://github.com/yourusername/telegram-bots.git
cd telegram-bots
```

2. Создать виртуальное окружение и установить зависимости:
```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux/macOS
# или
venv\Scripts\activate  # Для Windows
pip install -r requirements.txt
```

3. Настроить переменные окружения (см. раздел выше)

4. Запустить нужного бота:
```bash
python contact_bot.py  # Для бота сбора контактов
# или
python scam_bot.py     # Для скам-бота
```

### Установка на сервере

1. Клонировать репозиторий на сервер:
```bash
git clone https://github.com/yourusername/telegram-bots.git
cd telegram-bots
```

2. Установить зависимости:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Настроить переменные окружения (см. раздел выше)

4. Запустить бота в фоновом режиме:
```bash
# Установить screen, если его нет
apt install screen -y

# Создать новую screen-сессию
screen -S botname  # где botname - имя бота (contactbot или scambot)

# Запустить бота
python contact_bot.py  # или scam_bot.py

# Отсоединиться от сессии (Ctrl+A, затем D)
```

## Зависимости

- Python 3.7+
- aiogram 3.x (для contact_bot)
- pyTelegramBotAPI (для scam_bot)
- SQLite3 (встроен в Python)
- python-dotenv (для загрузки переменных окружения)