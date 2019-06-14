import json
import os
import requests
import random
import telegram
import map_logic
from telegram.ext import *

TOKEN = os.environ['telegram']

updater = Updater(token=TOKEN)

def init(bot,update):
    name = update.message.chat.first_name
    bot.send_message(chat_id=update.message.chat_id, text="Hi " + name + "!, How may i help? Might want to use /help for a start")


def getLoc(bot,update):
    try:
        loc_key = telegram.KeyboardButton(text="Send Current Location", request_location = True)
        keys = [[loc_key]]
        reply_markup = telegram.ReplyKeyboardMarkup(keys, resize_keyboard = True)
        bot.send_message(chat_id=update.message.chat_id, text="Share Location?", reply_markup=reply_markup)
    except Exception as e:
        print(e)


def help(bot,update):
     try:
        bot.send_message(chat_id=update.message.chat_id, text="Commands: /start, /getLoc                             \
        Enter <latitude,longitude> to query clusters manually")
     except Exception as e:
        print(e)


def current_loc_query(bot,update):
    try:
        print(update)
        bot.send_message(chat_id=update.message.chat_id, text="Here is the result for your current location")
        longitude = update.message.location.longitude
        latitude = update.message.location.latitude
        mh = map_logic.MapHandler(latitude,longitude)
        print(mh.result)

        if(mh.result == None):
            result = "No clusters found"
        else:
            result = mh.result

        bot.send_message(chat_id=update.message.chat_id, text=result)

    except Exception as e:
        print(e)


def manual_loc_query(bot,update):
    try:
        print(update)
        bot.send_message(chat_id=update.message.chat_id, text="Here is the result from manual query")
        text = update.message.text.split(",")
        latitude = float(text[0])
        longitude = float(text[1])
        mh = map_logic.MapHandler(latitude,longitude)
        print(mh.result)

        if(mh.result == None):
            result = "No clusters found"
        else:
            result = mh.result

        bot.send_message(chat_id=update.message.chat_id, text=result)

    except Exception as e:
        print(e)


# add the handlers
updater.dispatcher.add_handler(CommandHandler('start', init))
updater.dispatcher.add_handler(CommandHandler('getLoc', getLoc))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.location, current_loc_query))
updater.dispatcher.add_handler(MessageHandler(Filters.text, manual_loc_query))

updater.start_polling()

#allow exit with Ctrl + C
updater.idle()