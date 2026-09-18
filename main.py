import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configurazione log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Prendi il token da Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN non trovato! Mettilo nelle Environment Variables di Render")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao! 👋 Sono GiustCardBot\n\n"
        "Inviami una foto di una carta e ti dico:\n"
        "✅ Nome carta\n"
        "✅ Condizione stimata\n"
        "✅ Valore di mercato\n\n"
        "Invia pure la foto!"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Foto ricevuta! La sto analizzando... 🔍")
    
    # QUI VA LA TUA LOGICA DI VALUTAZIONE
    # Per ora risposta di test
    try:
        # Esempio: qui dovresti chiamare il tuo modello AI
        # photo_file = await update.message.photo[-1].get_file()
        # await photo_file.download_to_drive("card.jpg")
        
        await update.message.reply_text(
            "Analisi completata!\n\n"
            "Carta: Esempio - Charizard\n"
            "Condizione: Near Mint\n"
            "Valore stimato: 50-70€\n\n"
            "(Questa è una risposta di test, collega la tua AI qui)"
        )
    except Exception as e:
        logger.error(f"Errore: {e}")
        await update.message.reply_text(f"Errore durante l'analisi: {e}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    logger.info("Bot avviato...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
