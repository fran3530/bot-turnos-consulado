import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 
TOKEN = "8125132253:AAG-UgczuMp-fkgBxG_jgqzZKx--F4yu8u4
"
# 
CHAT_ID = 6791432578

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! Soy el bot para buscar turnos en el Consulado de España en Rosario.\n"
        "Usá /buscar para ver si hay turnos disponibles."
    )

# /buscar manual
async def buscar_turnos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(await revisar_turnos())

# 🔁 Revisión automática cada 20 minutos
async def revisar_turnos():
    url = "https://citaconsular.es/consulado/rosario" # Confirmá si esta es la URL correcta
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            turnos_div = soup.find(id='turnos') # Ajustá esto si el ID es otro
            if turnos_div:
                return f"✅ ¡Turnos disponibles!\n{turnos_div.get_text(strip=True)}"
            else:
                return "No hay turnos disponibles por ahora."
        else:
            return "⚠️ Error al conectar con la página."
    except Exception as e:
        return f"❌ Error: {e}"

# 👁️‍🗨️ Tarea de fondo para revisar automáticamente
async def tarea_periodica():
    bot = Bot(token=TOKEN)
    while True:
        mensaje = await revisar_turnos()
        if "✅" in mensaje:
            await bot.send_message(chat_id=CHAT_ID, text=mensaje)
        await asyncio.sleep(600) # Espera 10 minutos

# 🏁 Main
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buscar", buscar_turnos))

    # Inicia la tarea en segundo plano
    app.job_queue.run_once(lambda ctx: asyncio.create_task(tarea_periodica()), when=5)

    print("Bot corriendo...")
    app.run_polling()