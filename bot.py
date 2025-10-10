import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
from telegram.ext import ApplicationBuilder

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN env var is missing")

app = ApplicationBuilder().token(BOT_TOKEN).build()
# ... rest of your handlers and app.run_polling()

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bot is running successfully!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("✅ Screenshot received!")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
