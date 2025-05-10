import telebot
import time
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен из переменных окружения
TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Сообщение, которое будет отправляться пользователю
WARNING_MESSAGE = (
    "ОСТАНОВИСЬ.\n"
    "Это важно. Я не настоящий бот «Дари>Получай».\n"
    "Этот бот — копия, созданная, чтобы показать тебе одно:\n\n"
    "тебя обманывают.\n\n"
    "«Дари>Получай» — это финансовая пирамида.\n"
    "Она маскируется под добро, но работает по схеме, где старшие получают деньги от новых участников. Это не взаимопомощь. Это обман.\n\n"
    "📛 Никакие \"подарки\" просто так не работают.\n"
    "📛 Никакие боты не говорят правду, если они из этой системы.\n"
    "📛 Никакие красивые слова не вернут деньги, когда всё рухнет.\n\n"
    "👉 Забери свои деньги.\n"
    "👉 Удали этот бот и всех, кто тебя втянул.\n"
    "👉 Расскажи другим.\n"
    "👉 Будь свободен.\n\n"
    "Мы сделали этот бот, чтобы сказать тебе это.\n"
    "Будь осторожен. Ты достоин лучшего."
)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_warning(message):
    bot.send_message(message.chat.id, WARNING_MESSAGE)

# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def repeat_warning(message):
    bot.send_message(message.chat.id, WARNING_MESSAGE)

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