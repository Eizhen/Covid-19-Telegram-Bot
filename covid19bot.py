import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
import requests
from telegram.ext import MessageHandler, Filters
from telegram.ext import InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent


updater = Updater(token='Your Token', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Covid-19 updates")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()


def caps(update, context):
	summaryurl = "https://api.covid19api.com/summary"
	payload = {}
	headers= {}
	response = requests.request("GET", summaryurl, headers=headers, data = payload)
	print (response.json())
	globalupdate = response.json()['Global']
	update_text = "New Confirmed Cases: " + str(globalupdate['NewConfirmed']) + "\nTotal Confirmed Cases: " + str(globalupdate['TotalConfirmed']) + "\nNew Deaths: " + str(globalupdate['NewDeaths']) + "\nTotal Deaths: " + str(globalupdate['TotalDeaths']) + "\nNew Recovered: " + str(globalupdate['NewRecovered']) + "\nTotal Recovered: " + str(globalupdate['TotalRecovered'])

	context.bot.send_message(chat_id=update.effective_chat.id, text=update_text)

caps_handler = CommandHandler('updates', caps)
dispatcher.add_handler(caps_handler)
