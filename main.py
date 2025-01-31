import logging
import os
import nest_asyncio
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1) Allow nested event loop usage
nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)

# 2) Read the token from environment variable 'token_zb'
BOT_TOKEN = os.getenv("token_zb")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start handler
    Sends a message with an inline button that opens your miniapp inside Telegram.
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text="В Зарю 😊",
                web_app=WebAppInfo(url="https://belkinboris.github.io/zarya/")
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text="Привет! Мы рады тебя видеть! Чтобы продолжить, нажимай на кнопку ниже:",
        reply_markup=reply_markup
    )

async def main():
    # 3) Build the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # 4) Add the /start command handler
    application.add_handler(CommandHandler("start", start))

    # 5) Run the bot until you press Ctrl-C or the process is stopped
    await application.run_polling()

# 6) Re-use the existing event loop rather than creating a new one
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
