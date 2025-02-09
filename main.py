import logging
import os
import nest_asyncio
import asyncio

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
    MenuButtonWebApp
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# Разрешаем вложенные вызовы событий (актуально для локального запуска, Jupyter и т.д.)
nest_asyncio.apply()

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Читаем токен бота из переменной окружения "token_zb"
BOT_TOKEN = os.getenv("token_zb")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start handler
    Отправляем сообщение со встроенной кнопкой WebApp ("В Зарю 🌅").
    При нажатии кнопки Telegram откроет веб-приложение:
    - если домен подтверждён, то сразу в полноэкранном режиме;
    - иначе может показаться на половину экрана.
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text="В Зарю 🌅",
                web_app=WebAppInfo(url="https://belkinboris.github.io/zarya/")
                # ВАЖНО: URL должен совпадать с доменом, указанным в BotFather /setdomain
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text="Привет! Мы рады тебя видеть! Чтобы продолжить, нажми на кнопку ниже:",
        reply_markup=reply_markup
    )

async def main():
    """
    Точка входа.
    1. Создаём приложение-бот (Application).
    2. Ставим глобально Menu Button "Запуск" (MenuButtonWebApp).
    3. Регистрируем хендлер /start.
    4. Запускаем опрос обновлений (polling).
    """
    if not BOT_TOKEN:
        raise ValueError(
            "Токен бота не установлен. "
            "Убедитесь, что переменная окружения 'token_zb' содержит ваш bot token."
        )

    # Шаг 1. Создаём приложение бота
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Шаг 2. Настраиваем меню-кнопку (слева от поля ввода):
    #    - MenuButtonWebApp с текстом "Запуск",
    #    - Привязка к тому же URL (домену), что и в BotFather /setdomain.
    await application.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="Запуск",
            web_app=WebAppInfo(url="https://belkinboris.github.io/zarya/")
        )
    )

    # Шаг 3. Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Шаг 4. Запускаем бота (ожидаем Ctrl+C или остановки процесса)
    await application.run_polling()

# Шаг 5. Запуск main() в существующем event loop
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
