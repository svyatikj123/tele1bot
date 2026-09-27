import io
import telebot
from datetime import datetime
import psutil
# Инициализация бота с вашим токеном
bot = telebot.TeleBot('8876162909:AAGMh1SUrjw0T8PdpojVJ1nkvjoMG6UWQVU')

@bot.message_handler(commands=['report','start'])
def send_report(message):
    # 1. Формируем текст отчёта
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_content = f"--- АВТОМАТИЧЕСКИЙ ОТЧЁТ ---\n"
    report_content += f"Дата формирования: {current_time}\n"
    report_content += f"Статус системы: Работает стабильно\n"
    report_content += f"Данные: Все задачи на сегодня выполнены успешно.\n"

    # 2. Создаем файл в оперативной памяти (чтобы не сохранять на диск)
    report_file = io.BytesIO(report_content.encode('utf-8'))
    # Присваиваем имя файлу, которое увидит пользователь
    report_file.name = f"Report_{datetime.now().strftime('%Y%m%d')}.txt"

    # 3. Отправляем файл пользователю
    bot.send_message(message.chat.id, "Генерирую отчёт, подождите...")
    bot.send_document(message.chat.id, report_file)

@bot.message_handler(commands=['stats'])
def send_stats(message):
    # Получаем данные через psutil
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Форматируем сообщение
    text = (
        f"📊 **Состояние системы:**\n\n"
        f"💻 **ЦП (CPU):** {cpu_percent}%\n"
        f"🧠 **Оперативная память:** {memory.percent}% "
        f"(Использовано: {memory.used // (1024**2)} МБ / {memory.total // (1024**2)} МБ)\n"
        f"💾 **Диск (/):** {disk.percent}% "
        f"(Использовано: {disk.used // (1024**3)} ГБ / {disk.total // (1024**3)} ГБ)"
    )
    
    # Отправляем в чат с поддержкой Markdown
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                    "/start - отчёт в файле"
                    " /stats - отчёт в тексте"
                    " /report - отчёт в файле")

if __name__ == '__main__':
    print("Бот запущен и ждет команду /report...")
    bot.polling(none_stop=True)