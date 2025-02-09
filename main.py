import logging
import os
import nest_asyncio
import asyncio

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# Разрешаем вложенные вызовы event loop
nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)

# Читаем токен бота из переменной окружения
BOT_TOKEN = os.getenv("token_zb")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start.
    Просто выводим текст с инструкцией.
    """
    text = (
        "Привет! Мы рады тебя видеть!\n\n"
        "Чтобы запустить Зарю 🌅, перейдите в профиль (описание) нашего бота "
        "и там нажмите синюю кнопку «Запустить приложение». Удачи!"
    )
    await update.message.reply_text(text)

async def main():
    """
    Главная функция:
    1) создаём приложение;
    2) регистрируем /start;
    3) запускаем бота в режиме Polling.
    """
    if not BOT_TOKEN:
        raise ValueError("Не установлен токен бота. Убедитесь, что переменная окружения 'token_zb' содержит ваш токен.")

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем бот (polling)
    await application.run_polling()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
