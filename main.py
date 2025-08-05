import os
import threading
from flask import Flask
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- Configuration ---
TELEGRAM_TOKEN = '8111790144:AAHUcPi2SRaTO6A_kAjNbbnvUzYPVl3H85s'
GEMINI_API_KEY = 'AIzaSyBkW7xt1kk-r0jCGoy-8UQ06OrVPFlRwFY'


# --- Gemini Setup ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

# --- Telegram Message Handler ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    try:
        user_text = update.message.text
        gemini_response = chat.send_message(user_text)
        await update.message.reply_text(gemini_response.text)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# --- Run Telegram Bot in Background Thread ---
def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Telegram bot is running...")
    app.run_polling()

# Start the bot in a separate thread
threading.Thread(target=run_bot).start()

# --- Flask Web Server ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Gemini Telegram Bot is running!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render provides PORT
    web_app.run(host='0.0.0.0', port=port)
