import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# Токен от BotFather
API_TOKEN = '7779014860:AAEtePZABseH8HtkNr9DUikUzLaBry-K-4k'

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
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("База данных инициализирована")

# Функция для сохранения контакта в базу
def save_contact(user_id, first_name, username, phone_number):
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO contacts (user_id, first_name, username, phone_number) VALUES (?, ?, ?, ?)",
        (user_id, first_name, username, phone_number)
    )
    
    conn.commit()
    conn.close()
    print(f"Контакт сохранен: {first_name}, @{username}, {phone_number}")

# Создаем экземпляр бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    # Создаем клавиатуру с кнопкой "Поделиться контактом"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поделиться контактом", request_contact=True)]],
        resize_keyboard=True
    )
    
    # Отправляем сообщение с клавиатурой
    await message.reply(
        "Привет! Нажми кнопку ниже, чтобы поделиться своим контактом.",
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
    
    # Сохраняем в базу данных
    save_contact(user_id, first_name, username, phone_number)
    
    # Отправляем подтверждение пользователю
    await message.reply(
        f"Спасибо! Я сохранил твой контакт:\n"
        f"Имя: {first_name}\n"
        f"Никнейм: @{username}\n"
        f"Телефон: {phone_number}",
        reply_markup=ReplyKeyboardRemove()
    )

# Обработчик для обычного текста
@dp.message()
async def echo(message: types.Message):
    # Создаем клавиатуру с кнопкой "Поделиться контактом"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поделиться контактом", request_contact=True)]],
        resize_keyboard=True
    )
    
    await message.reply(
        "Пожалуйста, нажми кнопку ниже, чтобы поделиться своим контактом.",
        reply_markup=keyboard
    )

# Главная функция
async def main():
    # Инициализируем базу данных перед запуском бота
    init_db()
    
    # Запускаем бота
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())