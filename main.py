import os
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1. SETUP THE WEB SERVER (Required for Render)
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is active", 200

# 2. THE BOT LOGIC
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Change these URLs to your actual site later
    keyboard = [
        [InlineKeyboardButton("🚀 Clone This Bot", url="https://google.com")],
        [InlineKeyboardButton("🔑 Redeem API Key", url="https://google.com")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⚠️ *Authentication Required*\n\nYou are attempting to use the Clone Command. To proceed, please purchase an API key or redeem an existing one below.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# 3. THE "BRAIN" FUNCTION
def run_bot():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("CRITICAL ERROR: BOT_TOKEN variable is missing!")
        return
    
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clone", start))
    
    print("Telegram Bot started...")
    application.run_polling()

# Start the bot in a background thread
threading.Thread(target=run_bot, daemon=True).start()

# For local testing, but Render will use Gunicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
