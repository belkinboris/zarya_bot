import logging
import os
import nest_asyncio
import asyncio

from telegram import Update, MenuButtonDefault
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Разрешаем вложенные вызовы event loop (для локального запуска)
nest_asyncio.apply()

# Включаем базовое логирование
logging.basicConfig(level=logging.INFO)

# Считываем токен бота из переменной окружения 'token_zb'
BOT_TOKEN = os.getenv("token_zb")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start.
    Высылаем только текст, без кнопок WebApp.
    """
    text = (
        "Привет! Мы рады тебя видеть!\n\n"
        "Чтобы запустить Зарю 🌅, откройте профиль (описание) бота и нажмите "
        "синюю кнопку «Запустить приложение».\n\n"
        "Удачи!"
    )
    await update.message.reply_text(text)


async def main():
    """
    Главная функция:
    1) Создаём бота;
    2) Сбрасываем MenuButton в дефолтное (убираем «Запуск»);
    3) Регистрируем /start;
    4) Запускаем polling.
    """
    if not BOT_TOKEN:
        raise ValueError(
            "Не установлен токен бота. "
            "Убедитесь, что переменная окружения 'token_zb' содержит ваш bot token."
        )

    # 1. Создаём приложение (бот)
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # 2. Сбрасываем кнопку меню у бота на стандартную (убираем «Запуск»)
    await application.bot.set_chat_menu_button(
        menu_button=MenuButtonDefault()
    )

    # 3. Регистрируем /start
    application.add_handler(CommandHandler("start", start))

    # 4. Запускаем бота (polling)
    await application.run_polling()


if __name__ == "__main__":
    # Запускаем main() в текущем (асинхронном) event loop
    asyncio.run(main())
