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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and respond using Gemini."""
    if not update.message or not update.message.text:
        return
    
    try:
        user_text = update.message.text
        gemini_response = chat.send_message(user_text)
        await update.message.reply_text(gemini_response.text)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# --- Main ---
def main() -> None:
    """Start the bot."""
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()