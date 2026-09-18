import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ordini = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono GiustCardOrdiniBot attivo ✅\n\nComandi:\n/add - Aggiungi ordine\n/ordini - Lista ordini")

async def add_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ok, mandami l'ordine così:\nEs: Mario Rossi - 10 card Giust 1")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ordini.append(update.message.text)
    await update.message.reply_text(f"Ordine salvato! ✅\nTotale ordini: {len(ordini)}\nUsa /ordini per vederli")

async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ordini:
        await update.message.reply_text("Nessun ordine ancora.")
    else:
        testo = "\n".join([f"{i+1}. {o}" for i,o in enumerate(ordini)])
        await update.message.reply_text(f"📦 ORDINI GIUSTCARD:\n\n{testo}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_cmd))
app.add_handler(CommandHandler("ordini", lista))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
print("GiustCardOrdiniBot avviato")
app.run_polling()
