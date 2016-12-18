# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Обработка запросов про умный дом
# Автор: Ракитин Виталий
#

from constants import *
from Keyboards import *
from session import *


def send_information_about_clever_house_devices(bot,update,number):
    '''
    Посылаем информацию о конкретном девайсе с номером number,
    Сохраняем номер в сессию и спрашиваем, желает ли пользлователь 
    посмотреть изображение данного девайса
    '''
    update.message.reply_text(str(DEVICES_EMOJI[number])+RT_CLEVER_HOUSE_DEVICES[number]+str(DEVICES_EMOJI[number]))
    update.message.reply_text(RT_CLEVER_HOUSE_DEVICES_TEXT[number])
    update.message.reply_text("Хотите посмотреть, как он выглядит? (да/нет)",reply_markup = YES_NO_keyboard)
    save_device_in_session(update.message,number)
    return YES_NO_CHOICE


def send_photo_of_clever_house_devices(bot,message):
    '''Отправим фотографию девайся, номер хранится в сессии'''
    number = get_number_from_session(message.from_user.id)
    print number
    bot.send_photo(photo=open(RT_CLEVER_HOUSE_DEVICES_PATH[number], 'rb'),
                   chat_id=message.from_user.id)

def get_photo_or_not(bot, update):
    '''
    Выясняем у пользователя, хочет ли он посмотреть фотографию.
    Если хочет, то высылаем фото, и удаляем сессию;
    Если не хочет, удаляем сесиию, предложим посмотреть другие девайсы.
    '''
    text = update.message.text
    text = unicode(text.encode("utf-8"),"utf-8").encode("utf-8").lower() 

    if text == "да" or "да" in text:
    	send_photo_of_clever_house_devices(bot,update.message)
    	update.message.reply_text("Не желаете посмотреть про ещё какие-нибудь девайсы?",reply_markup = YES_NO_keyboard)
        kill_session(update.message.from_user.id)
        return YES_NO_CHOICE_TO_DEVICES

    elif text == "нет" or "нет" in text:
        update.message.reply_text("Хорошо! Не хотите посмотреть про ещё какие-нибудь девайсы?",reply_markup = YES_NO_keyboard)
        kill_session(update.message.from_user.id)
        return YES_NO_CHOICE_TO_DEVICES
    else: 
        update.message.reply_text("Я боюсь, что не могу Вас понять, давайте ещё раз попробуем!",reply_markup = YES_NO_keyboard)
        return YES_NO_CHOICE	

def house_information(bot, update):
    '''
    Выясняем, про какое устройство хотел бы узнать пользователь;
    '''
    print "Amigo"
    text = update.message.text
    text = unicode(text.encode("utf-8"),"utf-8").encode("utf-8").lower()

    if text == "1" or "контроллер" in text:
        return send_information_about_clever_house_devices(bot,update,0)
    elif text == "2" or "движения" in text:
        return send_information_about_clever_house_devices(bot,update,1)
    elif text == "3" or "открытия" in text:
        return send_information_about_clever_house_devices(bot,update,2)
    elif text == "4" or "протечки" in text:
        return send_information_about_clever_house_devices(bot,update,3)
    elif text == "5" or "дыма" in text:
        return send_information_about_clever_house_devices(bot,update,4)
    elif text == "6" or "розетка" in text:
        return send_information_about_clever_house_devices(bot,update,5)
    elif text == "7" or "лампочка" in text:
        return send_information_about_clever_house_devices(bot,update,6)
    else: 
        update.message.reply_text("Я боюсь, что не могу Вас понять, давайте ещё раз попробуем!",reply_markup = CleverHouse_keyboard)

    return HOME_INFO


def clever_house(bot, message):
    '''
    Выводим информацию об устройствах  
    '''
    text = ""
    for i,device in enumerate(RT_CLEVER_HOUSE_DEVICES):
        text += str(em.WHITE_HEAVY_CHECK_MARK) + "{0}. ".format(i+1) + device + ";\n"

    bot.send_message(message.from_user.id,RT_CLEVER_HOUSE_START)
    bot.send_message(message.from_user.id,text)
    bot.send_message(message.from_user.id,RT_CLEVER_HOUSE_MORE,reply_markup = CleverHouse_keyboard)
    return HOME_INFO


def clever_house_callback(bot, update):
    '''
    Выводим информацию об устройствах, запрошено из callback (inline keyboard)
    '''
    return clever_house(bot,update.callback_query)
	


def resend_devices(bot, update):
    '''
    Пользователь уже посмотрел на изображение девайся, 
    теперь он может посмотреть другие или вернуться в главное меню
    '''
    text = update.message.text
    text = unicode(text.encode("utf-8"),"utf-8").encode("utf-8").lower() 
    if text == "да" or "да" in text:
    	return clever_house(bot,update.message)

    update.message.reply_text(RT_SERVICES,reply_markup = RT_SERVICES_keyboard)
    return START_CONVERSATION
