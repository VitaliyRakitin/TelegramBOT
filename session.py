# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Обработка сессии
# Автор: Ракитин Виталий
#

from MySQL import *

def create_session(uid,datetime):
    '''Создать сессию'''
    tablename = "session{0}".format(uid)
    create_table(tablename,["datetime","message","answer"],["datetime","text","text"])
    args = (datetime, "start",None)  
    form = "%s,%s,%s"
    insert_into(tablename, form, args)


def add_message_in_session(uid,message):
    '''message = {datetime: datatime, text: text }'''
    tablename = "session{0}".format(uid)
    args = (message["datetime"],message["message"],message["answer"])  
    form = "%s,%s,%s"
    insert_into(tablename, form, args)


def kill_session(uid):
    '''Закрыть сессию'''
    tablename = "session{0}".format(uid)
    drop_table(tablename)



def save_device_in_session(message,number):
    '''Перед тем, как спросить пользователя о передаче ему изображения, 
    создаётся сессия, в которую записывается номер девайса, который он смотрел '''
    mymessage = {}
    mymessage["datetime"] = message.date
    mymessage["message"] = "YESNO"
    mymessage["answer"] = str(number)
    create_session(message.from_user.id,message.date)
    add_message_in_session(message.from_user.id,mymessage)


def get_number_from_session(uid):    
    '''достаём номер изображения из сессии'''
    tablename = "session{0}".format(uid)
    number = select_from_where("answer",tablename, "message","YESNO")[0]
    return int(number[0])
