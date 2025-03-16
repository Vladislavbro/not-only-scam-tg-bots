import telebot
import time
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен из переменных окружения
TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Обработчик всех входящих сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.lower() == "да":
        bot.reply_to(message, "Так и знал")
    else:
        bot.reply_to(message, "Сосал?")

# Сообщение о запуске бота
print("Бот успешно запущен! Нажмите Ctrl+C для остановки.")
print("Время запуска:", time.strftime("%H:%M:%S %d.%m.%Y"))
print("Ожидание сообщений...")

# Запуск бота (polling) с обработкой ошибок
try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"Произошла ошибка: {e}")
    print("Перезапуск бота через 5 секунд...")
    time.sleep(5)
    print("Бот перезапущен.")