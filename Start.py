# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Начало общения. Инициализация пользователя. Создание сессии.
# Автор: Ракитин Виталий
#

from DBProcessing import create_new_user, create_user_dict_from_db_answer, check_user_in_users_db
from session import create_session
from constants import *
from Keyboards import send_contact_keyboard,RT_SERVICES_keyboard
from CleverHouse import clever_house_callback

def start(bot, update):

    checkUserID, contact = check_user_in_users_db(update.message.from_user.id)

    if (checkUserID): 
        contact = create_user_dict_from_db_answer(contact)
        #create_session(update.message.from_user.id,update.message.date)
        update.message.reply_text(HELLO_KNOWN.format(contact["first_name"])+"!:)")
        update.message.reply_text(RT_SERVICES,reply_markup = RT_SERVICES_keyboard)
        return START_CONVERSATION
    else:
        update.message.reply_text(HELLO_NEW,reply_markup=send_contact_keyboard)
    return GET_CONTACT


def create_message_contact_dict(contact):
    print contact
    res = {}
    res["user_id"] = contact.user_id
    res["phone_number"] = contact.phone_number
    res["first_name"] = contact.first_name
    res["last_name"] = contact.last_name
    return res


def get_contact(bot, update):
    update.message.reply_text("Приятно познакомиться!\n")
    new_contact = create_message_contact_dict(update.message.contact)
    create_new_user(new_contact)
    #create_session(update.message.from_user.id,update.message.date)
    update.message.reply_text(RT_SERVICES,reply_markup = RT_SERVICES_keyboard)
    return START_CONVERSATION



def call_back(bot, update):
    '''
    Считываем информацию из главного меню
    '''
    if update.callback_query.data == "help":
        bot.send_message(update.callback_query.from_user.id,"Введите текст Вашего обращения:")
        update.callback_query.answer("Техподдержка")
        return NEED_HELP
    elif  update.callback_query.data == "internet":
        update.callback_query.answer("Интернет")
        return START_CONVERSATION #INTERNET_INFO
    elif  update.callback_query.data == "home":
        update.callback_query.answer("Умный дом")
        return clever_house_callback(bot, update)

    return START_CONVERSATION
