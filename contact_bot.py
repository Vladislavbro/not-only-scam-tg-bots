import asyncio
import sqlite3
import os
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен из переменных окружения
API_TOKEN = os.getenv("API_TOKEN")

# ID текущего мероприятия (по умолчанию 'default')
CURRENT_EVENT_ID = 'default'

# Функция для установки ID мероприятия при запуске
def setup_event_id():
    global CURRENT_EVENT_ID
    if len(sys.argv) > 1:
        CURRENT_EVENT_ID = sys.argv[1]
        print(f"ID мероприятия установлен: {CURRENT_EVENT_ID}")
    else:
        print(f"Используется ID мероприятия по умолчанию: {CURRENT_EVENT_ID}")

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    
    # Создаем таблицу, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        first_name TEXT,
        username TEXT,
        phone_number TEXT,
        event_id TEXT NOT NULL,
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("База данных инициализирована")

# Функция для сохранения контакта в базу
def save_contact(user_id, first_name, username, phone_number, event_id=None):
    if event_id is None:
        event_id = CURRENT_EVENT_ID
        
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO contacts (user_id, first_name, username, phone_number, event_id) VALUES (?, ?, ?, ?, ?)",
        (user_id, first_name, username, phone_number, event_id)
    )
    
    conn.commit()
    conn.close()
    print(f"Контакт сохранен: {first_name}, @{username}, {phone_number} для мероприятия {event_id}")

# Функция для проверки, отправлял ли пользователь контакт на текущем мероприятии
def has_shared_contact(user_id, event_id=None):
    if event_id is None:
        event_id = CURRENT_EVENT_ID
        
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT COUNT(*) FROM contacts WHERE user_id = ? AND event_id = ?",
        (user_id, event_id)
    )
    
    count = cursor.fetchone()[0]
    conn.close()
    
    return count > 0

# Создаем экземпляр бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    
    # Проверяем, отправлял ли пользователь контакт на текущем мероприятии
    if has_shared_contact(user_id):
        await message.reply(
            f"Спасибо! Вы уже отправили свой контакт для мероприятия {CURRENT_EVENT_ID}.",
            reply_markup=ReplyKeyboardRemove()
        )
        return
    
    # Создаем клавиатуру с кнопкой "Поделиться контактом"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Поделиться контактом", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    # Отправляем сообщение с клавиатурой
    await message.reply(
        f"Привет! Нажми кнопку ниже, чтобы поделиться своим контактом для мероприятия {CURRENT_EVENT_ID}.",
        reply_markup=keyboard
    )

# Обработчик получения контакта
@dp.message(lambda message: message.content_type == types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    contact = message.contact
    user = message.from_user
    
    # Получаем данные контакта
    user_id = user.id
    first_name = contact.first_name or "Не указано"
    username = user.username or "Не указано"
    phone_number = contact.phone_number
    
    # Проверяем, отправлял ли пользователь контакт на текущем мероприятии
    if has_shared_contact(user_id):
        await message.reply(
            f"Вы уже отправляли свой контакт для мероприятия {CURRENT_EVENT_ID}.",
            reply_markup=ReplyKeyboardRemove()
        )
        return
    
    # Сохраняем в базу данных
    save_contact(user_id, first_name, username, phone_number)
    
    # Отправляем подтверждение пользователю
    await message.reply(
        f"Спасибо! Я сохранил твой контакт для мероприятия {CURRENT_EVENT_ID}:\n"
        f"Имя: {first_name}\n"
        f"Никнейм: @{username}\n"
        f"Телефон: {phone_number}",
        reply_markup=ReplyKeyboardRemove()
    )

# Обработчик для обычного текста
@dp.message()
async def echo(message: types.Message):
    user_id = message.from_user.id
    
    # Проверяем, отправлял ли пользователь контакт на текущем мероприятии
    if has_shared_contact(user_id):
        await message.reply(
            f"Спасибо! Вы уже отправили свой контакт для мероприятия {CURRENT_EVENT_ID}.",
            reply_markup=ReplyKeyboardRemove()
        )
        return
    
    # Создаем клавиатуру с кнопкой "Поделиться контактом"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Поделиться контактом", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.reply(
        f"Пожалуйста, нажми кнопку ниже, чтобы поделиться своим контактом для мероприятия {CURRENT_EVENT_ID}.",
        reply_markup=keyboard
    )

# Главная функция
async def main():
    # Настраиваем ID мероприятия
    setup_event_id()
    
    # Инициализируем базу данных перед запуском бота
    init_db()
    
    # Запускаем бота
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())