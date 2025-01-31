import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

# Read the token from the environment variable 'token_zb'
BOT_TOKEN = os.getenv("token_zb")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start handler
    Sends a message with an inline button that opens your miniapp inside Telegram (WebApp).
    """
    # Inline keyboard with a single button that opens the miniapp via WebApp
    keyboard = [
        [
            InlineKeyboardButton(
                text="Open MiniApp",
                web_app=WebAppInfo(url="https://belkinboris.github.io/Zarya/")
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text="Hello! Click the button below to open the miniapp inside Telegram:",
        reply_markup=reply_markup
    )

async def main():
    # Build the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register the /start handler
    application.add_handler(CommandHandler("start", start))

    # Start polling
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
