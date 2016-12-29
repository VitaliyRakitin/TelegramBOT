#!/usr/bin/python 
# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Обработка сессии
# Автор: Ракитин Виталий
#

from MySQL import MySQL

class Sessions(object):
    def __init__(self):
        self.session_dict = {}
        self.CHOICE = "YESNO"
        self.DEVICE = "DEVICE"

    def create(self, uid): 
        self.session_dict[uid] = {}
        return self

    def add(self, uid, feature_name, feature):
        if uid not in self.session_dict:
            self.create(uid)
        self.session_dict[uid][feature_name] = feature
        return self

    def add_choice(self, uid, choice):
        self.add(uid, self.CHOICE, choice)

    def add_device(self, uid, device):
        self.add(uid, self.DEVICE, device)
    
    def get_choice(self, uid):
        return self.info(uid, self.CHOICE)

    def get_device(self, uid):
        return self.info(uid, self.DEVICE)

    def info(self, uid=None, feature = None):
        '''
        get information about sessions
        '''
        if uid:
            if uid in self.session_dict:
                if feature:
                    if feature in self.session_dict[uid]:
                        return self.session_dict[uid][feature]
                    return None
                return self.session_dict[uid]
            else:
                return None
        else: 
            return self.session_dict

    def drop(self, uid):
        if uid in self.session_dict:
            inform = self.session_dict.pop(uid)
        return self

if __name__ == "__main__":
    sess = Sessions()
    sess.create(100)
    print sess.info(100)
    print sess.info(111)
    sess.drop(111)
    sess.drop(100)

def create_session(uid,datetime):
    '''Создать сессию'''
    tablename = "session{0}".format(uid)
    MySQL().create_table(tablename,["datetime","message","answer"],["datetime","text","text"])
    args = (datetime, "start",None)  
    form = "%s,%s,%s"
    MySQL().insert_into(tablename, form, args)


def add_message_in_session(uid,message):
    '''message = {datetime: datatime, text: text }'''
    tablename = "session{0}".format(uid)
    args = (message["datetime"],message["message"],message["answer"])  
    form = "%s,%s,%s"
    MySQL().insert_into(tablename, form, args)


def kill_session(uid):
    '''Закрыть сессию'''
    tablename = "session{0}".format(uid)
    MySQL().drop_table(tablename)



def save_device_in_session(bot, message, number):
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
    number = MySQL().select_from_where(["answer"],tablename, "message","YESNO")[0]
    return int(number[0])
