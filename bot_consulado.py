import telebot

TOKEN = "8125132253:AAG-UgczuMp-fkgBxG_jgqzZKx--F4yu8u4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy tu bot para ayudarte con los turnos del consulado. ¿Qué necesitás?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Recibí tu mensaje: " + message.text)

bot.infinity_polling()