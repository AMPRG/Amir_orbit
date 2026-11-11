import os
import threading
import requests
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# تنظیمات اتصال به API جدید شما (Dahl / MiniMax)
DAHL_API_KEY = os.environ.get("DAHL_API_KEY")
DAHL_URL = "https://inference.dahl.global/v1/chat/completions"

def call_ai_api(prompt_text):
    headers = {
        "Authorization": f"Bearer {DAHL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "MiniMaxAI/MiniMax-M2.7",
        "messages": [
            {
                "role": "system",
                "content": "تو یک دستیار آموزشی و درسی هوشمند هستی. به سوالات درسی به زبان فارسی و به صورت دقیق و مفهومی پاسخ بده."
            },
            {
                "role": "user",
                "content": prompt_text
            }
        ]
    }
    try:
        response = requests.post(DAHL_URL, json=payload, headers=headers)
        res_data = response.json()
        return res_data["choices"]["message"]["content"]
    except Exception as e:
        print(f"API Error: {e}")
        return "متأسفانه در ارتباط با هوش مصنوعی خطایی رخ داد."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id
    
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    reply_text = call_ai_api(user_message)
    await update.message.reply_text(reply_text)

def main():
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)

    application.run_polling()

if __name__ == '__main__':
    t = threading.Thread(target=run_flask)
    t.start()
    main()
