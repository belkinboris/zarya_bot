import logging
import os
import nest_asyncio
import asyncio

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# Разрешаем многократные и вложенные вызовы event loop (для локального запуска)
nest_asyncio.apply()

# Включаем базовый логгер
logging.basicConfig(level=logging.INFO)

# Пример: читаем токен бота из переменной окружения 'token_zb'
# Убедитесь, что токен действительно выставлен: export token_zb="12345:YOUR_BOT_TOKEN"
BOT_TOKEN = os.getenv("token_zb")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start.
    Отправляет приветственное сообщение с кнопкой «В Зарю».
    
    При нажатии кнопки:
    - Telegram открывает mini-app (WebApp),
    - Если домен подтверждён в BotFather, 
      будет popup «By launching this Mini App…» 
      и приложение запустится на весь экран.
    """
    # Кнопка с web_app=WebAppInfo(...) говорит Телеграму,
    # что нужно открыть именно мини-приложение, а не просто URL
    keyboard = [
        [
            InlineKeyboardButton(
                text="В Зарю 🌅",
                # ВАЖНО: укажите тут ваш реальный URL, 
                # который зарегистрирован в BotFather как домен мини-приложения
                web_app=WebAppInfo(url="https://belkinboris.github.io/zarya/")
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text=(
            "Привет! Мы рады тебя видеть!\n\n"
            "Нажми на кнопку, чтобы открыть мини-приложение 'Заря'!"
        ),
        reply_markup=reply_markup
    )


async def main():
    """
    Точка входа в программу.
    Создаём Application, регистрируем обработчики и запускаем бота в режиме polling.
    """
    if not BOT_TOKEN:
        raise ValueError("Не установлен токен бота. "
                         "Убедитесь, что переменная окружения 'token_zb' задана.")

    # Создаём приложение (бот)
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Добавляем команду /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота (блокирующий вызов, до Ctrl+C)
    await application.run_polling()

    
if __name__ == "__main__":
    # Запускаем main() в текущем event loop
    asyncio.get_event_loop().run_until_complete(main())
