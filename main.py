import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")

FILE_CARTA = "ultima_carta.txt"

def salva_carta(nome):
    with open(FILE_CARTA, "w", encoding="utf-8") as f:
        f.write(nome)

def leggi_carta():
    try:
        with open(FILE_CARTA, "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    carta = leggi_carta()
    if carta:
        await update.message.reply_text(
            f"Guarda hai ordinato la carta di {carta} ieri, "
            f"oggi è arrivata e nel magazzino hai solo quella."
        )
    else:
        await update.message.reply_text(
            "Ciao! Al momento nessuna carta nuova arrivata in magazzino."
        )

async def arrivata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usa così: /arrivata Paperino")
        return
    nome_carta = " ".join(context.args)
    salva_carta(nome_carta)
    await update.message.reply_text(f"Fatto! ✅ Impostata come arrivata: {nome_carta}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("arrivata", arrivata))
    # per compatibilità se il cliente scrive /saldo o /prezzo
    app.add_handler(CommandHandler("saldo", start))
    app.add_handler(CommandHandler("prezzo", start))
    print("Bot avviato...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
