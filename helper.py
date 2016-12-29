#!/usr/bin/python 
# -*- coding: utf-8 -*-
#
# Телеграм Бот 
# Техподдержка
# Автор: Ракитин Виталий
#
# Искуственный интеллект распознавания запросов.
# Если бот не может ответить на вопрос, то он сохраняется в базе данных.
#

from DB import NotificationsDB
from Learning import Learning
from constants import Replies as rp
from constants import States as st
from Keyboards import Keyboards as kb

class Helper(object):
    def __init__(self, session):
        self.session = session
        self.NO_SUCH_ANSWER = -1
        self.learn = Learning()
        self.learn.fit()
        self.ntf = NotificationsDB()
        self.SORRY = rp.SORRY_NO_ANSWER


    def helper(self, bot, update):
        '''
        собственно помошник
        '''
        text = update.message.text
        text = unicode(text.encode("utf-8"),"utf-8").encode("utf-8").lower() 
        answer = self.learn.predict(text)

        if answer == self.NO_SUCH_ANSWER:
            self.create_notification(update.message)
            notification = self.create_notification(update.message)
            self.ntf.send_notification(notification)
            update.message.reply_text(self.SORRY)
        else:
            update.message.reply_text(answer[0])
            update.message.reply_text(answer[1])

        update.message.reply_text(rp.RT_SERVICES_LIST,reply_markup = kb.RT_SERVICES_KEYBOARD)
        return st.START_CONVERSATION


    @staticmethod
    def create_notification(message):
        '''
        Из стандартного типа message создаём notification,
        чтобы внести запрос в базу
        '''
        notification = {}
        notification["user_id"] = message.chat.id
        notification["notification"] = message.text
        notification["date"] = message.date
        return notification


if __name__ == "__main__":
    pass