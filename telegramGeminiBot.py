import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# --- Configuration ---
TELEGRAM_TOKEN = '8111790144:AAHUcPi2SRaTO6A_kAjNbbnvUzYPVl3H85s'
GEMINI_API_KEY = 'AIzaSyBkW7xt1kk-r0jCGoy-8UQ06OrVPFlRwFY'

# --- Gemini Setup ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # Use the model you prefer
chat = model.start_chat()

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm your Gemini-powered bot 🤖. Ask me anything!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    gemini_response = chat.send_message(user_text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=gemini_response.text)

# --- Main ---
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
