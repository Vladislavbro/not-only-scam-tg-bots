import telebot
import time

# Не забудьте заменить токен на свой, храните его в секрете!
TOKEN = '7779014860:AAEtePZABseH8HtkNr9DUikUzLaBry-K-4k'
bot = telebot.TeleBot(TOKEN)

# Обработчик всех входящих сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
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