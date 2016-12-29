#!/usr/bin/python 
# -*- coding: utf-8 -*-
#
# Телеграм Бот 
# Начало общения. Инициализация пользователя. Создание сессии.
# Автор: Ракитин Виталий
#

from DB import UsersDB

from constants import Replies as rp 
from constants import States as st
from Keyboards import Keyboards as kb


class Start(object):


    def __init__(self, CleverHouse, sessions):
        self.ch = CleverHouse
        self.sessions = sessions
        self.db = UsersDB()
        self.HELP = "help"
        self.INTERNET = "internet"
        self.HOUSE = "home"

        self.HELP_RU = "Техподдержка"
        self.INTERNET_RU = "Интернет"
        self.HOUSE_RU = "Умный дом"

        self.UID = "user_id"
        self.PHONE = "phone_number"
        self.FIRST_NAME = "first_name"
        self.LAST_NAME = "last_name"


    def start(self, bot, update):

        checkUserID, contact = self.db.check_user_in_db(update.message.chat.id)
        self.sessions.create(update.message.chat.id)

        if (checkUserID): 
            contact = self.db.create_user_dict_from_db_answer(contact)
            update.message.reply_text(rp.HELLO_KNOWN_USER.format(contact[self.FIRST_NAME]) + "!:)")
            update.message.reply_text(rp.RT_SERVICES_LIST, reply_markup = kb.RT_SERVICES_KEYBOARD)
            return st.START_CONVERSATION
        else:
            update.message.reply_text(rp.HELLO_NEW_USER, reply_markup = kb.SEND_CONTACT_KEYBOARD)
        return st.GET_CONTACT

    
    def create_contact_dict_from_message(self, contact):
        contact_dict = {}
        contact_dict[self.UID] = contact.user_id
        contact_dict[self.PHONE] = contact.phone_number
        contact_dict[self.FIRST_NAME] = contact.first_name
        contact_dict[self.LAST_NAME] = contact.last_name
        return contact_dict


    def get_contact(self, bot, update):
        update.message.reply_text(rp.NICE_TO_MEET_YOU)
        new_contact = self.create_contact_dict_from_message(update.message.contact)
        self.db.create_new_user(new_contact)
        update.message.reply_text(rp.RT_SERVICES_LIST,reply_markup = kb.RT_SERVICES_KEYBOARD)
        return st.START_CONVERSATION


    def call_back(self, bot, update):
        '''
        Считываем информацию из главного меню
        '''
        if update.callback_query.data == self.HELP:
            bot.send_message(update.callback_query.message.chat.id,rp.PRINT_YOUR_REQUESR)
            update.callback_query.answer(self.HELP_RU)
            return st.NEED_HELP

        elif update.callback_query.data == self.INTERNET:
            update.callback_query.answer(self.INTERNET_RU)
            return st.START_CONVERSATION #INTERNET_INFO

        elif  update.callback_query.data == self.HOUSE:
            update.callback_query.answer(self.HOUSE_RU)
            return self.ch.clever_house_callback(bot, update)

        return st.START_CONVERSATION
if __name__ == "__main__":
    print Start().HELP