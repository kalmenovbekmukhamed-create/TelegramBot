# bot.py (Corrected and Merged)

import os
import io
import re
import numpy as np
import cv2
import pytesseract
from dataclasses import dataclass
from typing import List, Optional

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- Your Tesseract Path for the Server ---
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# --- Get Token ---
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN env var is missing")

# ===================================================================
# PASTE ALL THE HELPER CODE FROM THE ORIGINAL SCRIPT HERE
#
# This includes:
# - All the @dataclass definitions (Candle, Px2Price)
# - All the tunable settings (HSV_GREEN, HSV_RED, etc.)
# - The ocr_right_price_scale() function
# - The fallback_last_price() function
# - The detect_bodies() function
# - The recent_swing_prices() function
# - The decide_signal() function
#
# ===================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running successfully! Send a screenshot.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This is the function that now does the real work."""
    try:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        b = await file.download_as_bytearray()
        img = cv2.imdecode(np.frombuffer(b, np.uint8), cv2.IMREAD_COLOR)

        # --- Call the analysis functions ---
        px2p = ocr_right_price_scale(img)
        candles = detect_bodies(img)
        side, entry, sl, tps = decide_signal(candles, px2p, img)

        debug = f"candles={len(candles)} | mapping={'ok' if px2p else 'fail'}"
        msg = (
            f"🧠 Screenshot Analysis\n"
            f"• Side: {side}\n"
            f"• Entry: {entry if entry is not None else '—'}\n"
            f"• SL: {sl if sl is not None else '—'}\n"
            f"• TP: {tps if tps else '—'}\n"
            f"• Debug: {debug}\n"
            f"— Not financial advice."
        )
        await update.message.reply_text(msg)

    except Exception as e:
        print("Error in handle_photo:", e) # This will print the error to our server logs
        await update.message.reply_text(f"⚠️ An error occurred during image processing: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
