import os, json, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
DATA_FILE = "data.json"
OWNER_ID = 7913369613

app_flask = Flask(__name__)
@app_flask.route("/")
def home():
    return "Bot Giustcard attivo!"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Invia una foto di una carta per valutarla. Usa /saldo /prezzo /help")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - Avvia\n/saldo - Vedi saldo\n/prezzo - Prezzo carta\nInvia foto carta per valutarla")

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    uid = str(update.effective_user.id)
    s = data.get(uid, {}).get("saldo", 0)
    await update.message.reply_text(f"Il tuo saldo: {s}€")

async def prezzo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Invia la foto della carta e ti dico il prezzo!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Foto ricevuta! Sto valutando... (funzione valutazione in arrivo)\nIl tuo saldo è stato aggiornato!")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot avviato...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(CommandHandler("saldo", saldo))
    application.add_handler(CommandHandler("prezzo", prezzo))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.run_polling()
