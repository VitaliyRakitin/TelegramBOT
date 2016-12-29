#!/usr/bin/python 
# -*- coding: utf-8 -*-
#
# Телеграм Бот 
# Обработка запросов про умный дом
# Автор: Ракитин Виталий
#

from constants import Replies as rp
from constants import States as st
from constants import DEVICES_EMOJI as em
from constants import WHITE_HEAVY_CHECK_MARK
from Keyboards import Keyboards as kb
from DB import DevicesDB

class CleverHouse(object):
    
    def __init__(self, sessions):
        self.sessions = sessions
        self.db = DevicesDB()


    def send_information_about_device(self, bot, update, number):
        '''
        Посылаем информацию о конкретном девайсе с номером number,
        Сохраняем номер в сессию и спрашиваем, желает ли пользлователь 
        посмотреть изображение данного девайса
        '''

        device, description = self.db.get_description(number)
        device = device.encode("utf-8")
        description = description.encode("utf-8")
        update.message.reply_text(em[number] + device + em[number])
        update.message.reply_text(description)
        update.message.reply_text(rp.WOULD_YOU_LIKE_TO_SEE_IT,reply_markup = kb.YES_NO_KEYBOARD)
        print number
        self.sessions.add_device(update.message.from_user.id, number)
        return st.YES_NO_CHOICE


    def send_photo_of_clever_house_devices(self, bot, message):
        '''Отправим фотографию девайся, номер хранится в сессии'''
        number = self.sessions.get_device(message.from_user.id)
        photo_path = self.db.get_img_path(number).encode("utf-8")
        bot.send_photo( photo=open(photo_path, 'rb'),
                        chat_id=message.from_user.id)

    def get_photo_or_not(self, bot, update):
        '''
        Выясняем у пользователя, хочет ли он посмотреть фотографию.
        Если хочет, то высылаем фото, и удаляем сессию;
        Если не хочет, удаляем сесиию, предложим посмотреть другие девайсы.
        '''
        text = update.message.text
        text = unicode(text.encode("utf-8"),"utf-8").encode("utf-8").lower() 

        if text == "да" or "да" in text:
            self.send_photo_of_clever_house_devices(bot, update.message)
            update.message.reply_text(rp.ANY_MORE_DEVICES, reply_markup = kb.YES_NO_KEYBOARD)
            return st.YES_NO_CHOICE_TO_DEVICES

        elif text == "нет" or "нет" in text:
            update.message.reply_text(rp.OK + rp.ANY_MORE_DEVICES,reply_markup = kb.YES_NO_KEYBOARD)
            return st.YES_NO_CHOICE_TO_DEVICES
        else: 
            update.message.reply_text(rp.DONT_UNDERSTAND,reply_markup = kb.YES_NO_KEYBOARD)
            return st.YES_NO_CHOICE    

    def house_information(self, bot, update):
        '''
        Выясняем, про какое устройство хотел бы узнать пользователь;
        '''
        text = update.message.text
        text = unicode(text.encode("utf-8"),"utf-8").encode("utf-8").lower()

        if text == "1" or "контроллер" in text:
            return self.send_information_about_device(bot,update,0)
        elif text == "2" or "движения" in text:
            return self.send_information_about_device(bot,update,1)
        elif text == "3" or "открытия" in text:
            return self.send_information_about_device(bot,update,2)
        elif text == "4" or "протечки" in text:
            return self.send_information_about_device(bot,update,3)
        elif text == "5" or "дыма" in text:
            return self.send_information_about_device(bot,update,4)
        elif text == "6" or "розетка" in text:
            return self.send_information_about_device(bot,update,5)
        elif text == "7" or "лампочка" in text:
            return self.send_information_about_device(bot,update,6)
        else: 
            update.message.reply_text(rp.DONT_UNDERSTAND,reply_markup = kb.CLEVER_HOUSE_KEYBOARD)

        return st.HOME_INFO


    def clever_house(self, bot, message):
        '''
        Выводим информацию об устройствах  
        '''
        text = ""
        devices = self.db.get_devices()
        for i,device in devices:
            device = device.encode("utf-8")
            text += WHITE_HEAVY_CHECK_MARK + "{0}. ".format(i+1) + device + ";\n"

        bot.send_message(message.from_user.id,rp.RT_CLEVER_HOUSE_START)
        bot.send_message(message.from_user.id,text)
        bot.send_message(message.from_user.id,rp.RT_CLEVER_HOUSE_MORE,reply_markup = kb.CLEVER_HOUSE_KEYBOARD)
        return st.HOME_INFO


    def clever_house_callback(self, bot, update):
        '''
        Выводим информацию об устройствах, запрошено из callback (inline KEYBOARD)
        '''
        return self.clever_house(bot, update.callback_query)
    


    def resend_devices(self, bot, update):
        '''
        Пользователь уже посмотрел на изображение девайся, 
        теперь он может посмотреть другие или вернуться в главное меню
        '''
        text = update.message.text
        text = unicode(text.encode("utf-8"),"utf-8").encode("utf-8").lower() 
        if text == "да" or "да" in text:
           return self.clever_house(bot,update.message)

        update.message.reply_text(rp.RT_SERVICES_LIST,reply_markup = kb.RT_SERVICES_KEYBOARD)
        print self.sessions.info(update.message.from_user.id)
        return st.START_CONVERSATION
