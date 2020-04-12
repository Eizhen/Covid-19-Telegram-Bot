import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
import requests
from telegram.ext import MessageHandler, Filters
from telegram.ext import InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler


bot = telegram.Bot(token='Your Token')


"""byCountryUrl = "https://api.covid19api.com/dayone/country/south-africa"
payload = {}
headers= {}
response = requests.request("GET", byCountryUrl, headers=headers, data = payload)
print (response.json())"""

countryurl = "https://api.covid19api.com/countries"




updater = Updater(token='Your Token', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)



"""custom_keyboard = [['/summary', 'start'], 
                   ['bottom-left', 'bottom-right']]
reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

"""

button_list = [
    [
        InlineKeyboardButton("start", callback_data='/start'),
        InlineKeyboardButton("summary", callback_data='/summary')
    ],
    [
        InlineKeyboardButton("picture", callback_data='/pic')
    ]
]


reply_markup = InlineKeyboardMarkup(button_list)
#bot.send_message(..., "A two-column menu", reply_markup=reply_markup)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,text="Covid-19 updates", reply_markup=reply_markup)
    #reply_markup = telegram.ReplyKeyboardRemove()
    #bot.send_message(chat_id=update.effective_chat.id, text="I'm back.", reply_markup=reply_markup)
    #context.bot.send_message(chat_id=update.effective_chat.id, 
                # text="Covid-19 updates", 
                # reply_markup=reply_markup)
    #context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('coronavirus.jpg', 'rb'))

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)





def summary(update, context):
	summaryurl = "https://api.covid19api.com/summary"
	payload = {}
	headers= {}
	response = requests.request("GET", summaryurl, headers=headers, data = payload)
	print (response.json())
	globalupdate = response.json()['Global']
	summary_text = "New Confirmed Cases: " + str(globalupdate['NewConfirmed']) + "\nTotal Confirmed Cases: " + str(globalupdate['TotalConfirmed']) + "\nNew Deaths: " + str(globalupdate['NewDeaths']) + "\nTotal Deaths: " + str(globalupdate['TotalDeaths']) + "\nNew Recovered: " + str(globalupdate['NewRecovered']) + "\nTotal Recovered: " + str(globalupdate['TotalRecovered'])

	context.bot.send_message(chat_id=update.effective_chat.id, text=summary_text, reply_markup=reply_markup)

summary_handler = CommandHandler('summary', summary)
dispatcher.add_handler(summary_handler)


def pic(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('coronavirus.jpg', 'rb'), reply_markup=reply_markup)

pic_handler = CommandHandler('pic', pic)
dispatcher.add_handler(pic_handler)


dispatcher.add_handler(CallbackQueryHandler(start, pattern="/start"))
dispatcher.add_handler(CallbackQueryHandler(summary, pattern="/summary"))
dispatcher.add_handler(CallbackQueryHandler(pic, pattern="/pic"))

def unknownText(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that.", reply_markup=reply_markup)

unknown_text_handler = MessageHandler(Filters.text, unknownText)
dispatcher.add_handler(unknown_text_handler)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.", reply_markup=reply_markup)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


updater.start_polling()
