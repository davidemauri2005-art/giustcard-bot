import os
from flask import Flask
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ordini = []

app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "Bot Giustcard Attivo!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono GiustCard Bot! Invia un ordine.")

async def add_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ok, ordine ricevuto! Scrivilo per esteso.")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    testo = update.message.text
    ordini.append(testo)
    await update.message.reply_text(f"Ordine salvato: {testo}")

async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ordini:
        await update.message.reply_text("Nessun ordine.")
    else:
        await update.message.reply_text("\n".join(ordini))

def run_web():
    app_web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__ == '__main__':
    threading.Thread(target=run_web, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_cmd))
    app.add_handler(CommandHandler("lista", lista))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    print("Bot avviato...")
    app.run_polling()
