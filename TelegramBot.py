# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Автор: Ракитин Виталий
#

from Keyboards import *
from constants import *
from session import kill_session

from config import BOT_TOKEN

from Start import (start, get_contact,call_back)
from CleverHouse import (house_information,get_photo_or_not,resend_devices)
from telegram.emoji import Emoji as em

from telegram.ext import (Updater, CommandHandler, MessageHandler,CallbackQueryHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

from helper import helper

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def create_message_dict(message):
    res = {}
    res["text"] = message.text
    res["datetime"] = message.date
    return res


def get_text(bot, update):
    message = create_message_dict(update.message)
    #add_message_in_session(update.message.from_user.id,message)
    update.message.reply_text("Выберети, пожалуйста пункт, который Вы бы хотели обсудить!")
    return START_CONVERSATION

def internet(bot, update):
    message = create_message_dict(update.message)
    #add_message_in_session(update.message.from_user.id,message)
    update.message.reply_text("Да, мы предоставляем интернет!")
    return START_CONVERSATION


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))




def done(bot, update):
    kill_session(update.message.from_user.id)
    update.message.reply_text("До свидания, был рад Вас видеть!")
    return ConversationHandler.END


# Create the Updater and pass it your bot's token.
updater = Updater(BOT_TOKEN)

# Get the dispatcher to register handlers
dp = updater.dispatcher

# Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      MessageHandler(Filters.text,start)],
    
        states={
            GET_CONTACT: [MessageHandler(Filters.contact, get_contact),],
            START_CONVERSATION: [ MessageHandler(Filters.text,get_text),
                                  CallbackQueryHandler(call_back)],
            HOME_INFO: [MessageHandler(Filters.text, house_information),],
            YES_NO_CHOICE: [MessageHandler(Filters.text, get_photo_or_not),],
            YES_NO_CHOICE_TO_DEVICES: [MessageHandler(Filters.text, resend_devices)],
            NEED_HELP: [MessageHandler(Filters.text, helper)]
        },
        fallbacks = [CommandHandler('done', done)]
        )



dp.add_handler(conv_handler)

dp.add_handler(CommandHandler('done', done))
dp.add_handler(CommandHandler('start', start))
#dp.add_handler(CallbackQueryHandler(call_back))
# log all errors
dp.add_error_handler(error)

# Start the Bot
updater.start_polling()

# Run the bot until the you presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()





