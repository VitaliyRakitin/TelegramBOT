# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Автор: Ракитин Виталий
#

from Keyboards import Keyboards
from constants import States as st
from session import kill_session

from config import BOT_TOKEN

from Start import Start 
from CleverHouse import CleverHouse
from telegram.emoji import Emoji as em

from telegram.ext import (Updater, CommandHandler, MessageHandler,CallbackQueryHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

from helper import Helper

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
class TelegramBot:
    '''
    Главный класс бота
    '''

    def __init__(self, token):
        self.House = CleverHouse()
        self.house_information = self.House.house_information
        self.get_photo_or_not = self.House.get_photo_or_not
        self.resend_devices = self.House.resend_devices

        self.Start = Start(self.House)
        self.start = self.Start.start
        self.get_contact = self.Start.get_contact
        self.call_back = self.Start.call_back

        self.helper = Helper().helper

        self.updater = Updater(token) #BOT_TOKEN
        self.dispatcher = self.updater.dispatcher
        self.create_handlers()
        self.add_handlers()
        self.fit()

    def fit(self):
        self.helper = Helper().helper

    def create_handlers(self):
        self.main_handler = ConversationHandler(
                                entry_points =
                                [   CommandHandler('start', self.start),
                                    MessageHandler(Filters.text,self.start),
                                ],
                                
                                states = 
                                {
                                    st.GET_CONTACT: [MessageHandler(Filters.contact, self.get_contact),],
                                    st.START_CONVERSATION: [ MessageHandler(Filters.text,self.get_text),
                                                          CallbackQueryHandler(self.call_back)],
                                    st.HOME_INFO: [MessageHandler(Filters.text, self.house_information),],
                                    st.YES_NO_CHOICE: [MessageHandler(Filters.text, self.get_photo_or_not),],
                                    st.YES_NO_CHOICE_TO_DEVICES: [MessageHandler(Filters.text, self.resend_devices)],
                                    st.NEED_HELP: [MessageHandler(Filters.text, self.helper)]
                                },
                                
                                fallbacks = 
                                [   CommandHandler('done', self.done)]
                            )
        return self

    def add_handlers(self):
        self.dispatcher.add_handler(self.main_handler)
        self.dispatcher.add_handler(CommandHandler('done', self.done))
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_error_handler(self.error)
        return self

    def run(self):
        # Start the Bot
        self.updater.start_polling()

        # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()

    #def create_message_dict(message):
    #    res = {}
    #    res["text"] = message.text
    #    res["datetime"] = message.date
    #    return res

    @staticmethod
    def get_text(bot, update):
        #message = create_message_dict(update.message)
        #add_message_in_session(update.message.from_user.id,message)
        update.message.reply_text("Выберети, пожалуйста пункт, который Вы бы хотели обсудить!")
        return st.START_CONVERSATION

    @staticmethod
    def internet(bot, update):
        message = create_message_dict(update.message)
        #add_message_in_session(update.message.from_user.id,message)
        update.message.reply_text("Да, мы предоставляем интернет!")
        return st.START_CONVERSATION

    @staticmethod
    def error(bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))

    @staticmethod
    def done(bot, update):
        kill_session(update.message.from_user.id)
        update.message.reply_text("До свидания, был рад Вас видеть!")
        return ConversationHandler.END



if __name__ == "__main__":
    bot = TelegramBot(BOT_TOKEN)
    bot.run()




