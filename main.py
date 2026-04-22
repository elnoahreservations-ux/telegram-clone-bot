import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Replace with your actual website link
WEBSITE_URL = "https://your-infinityfree-link.com"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Clone A Bot", url=f"{WEBSITE_URL}/purchase.html")],
        [InlineKeyboardButton("🔑 Redeem API Key", url=f"{WEBSITE_URL}/redeem.html")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⚠️ *Access Denied*\n\nTo use the Clone Command, you must have an active API Key.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

if __name__ == '__main__':
    # We get the token from Render Environment Variables later
    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clone", start))
    
    print("Bot is running...")
    app.run_polling()
