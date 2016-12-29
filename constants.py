#!/usr/bin/python 
# -*- coding: utf-8 -*-
#
# Телеграм Бот 
# Глобальные константы
# Автор: Ракитин Виталий
#

from telegram.emoji import Emoji as em


#-------------- states ---------------#
class States(object):
    [GET_CONTACT, START_CONVERSATION, NEED_HELP, 
    INTERNET_INFO, HOME_INFO, YES_NO_CHOICE, 
    YES_NO_CHOICE_TO_DEVICES] = range(7)



#-------------- emoji --------------#


DEVICES_EMOJI = [
    str(em.MOBILE_PHONE),
    str(em.RUNNER),
    str(em.CLOSED_LOCK_WITH_KEY),
    str(em.POTABLE_WATER_SYMBOL),
    str(em.FIRE),
    str(em.ELECTRIC_PLUG),
    str(em.ELECTRIC_LIGHT_BULB)
    ]

WHITE_HEAVY_CHECK_MARK = str(em.WHITE_HEAVY_CHECK_MARK)


#-------------- answers --------------#

class Replies():
    SORRY_NO_ANSWER = "Извините, к сожалению, я не могу сейчас ответить на Ваш вопрос! Он уже передан в техподдержку! Вам обязательно перезвонят!"
    HELLO_NEW_USER =  "Добрый день!\nВас приветствует telegram-bot компании Ростелеком!\nДавайте познакомимся, для упрощения общения, предлагаю Вам просто выслать Ваши контактные данные. :)"
    HELLO_KNOWN_USER = "Добрый день,{0}!\nРад снова Вас видеть!"
    RT_SERVICES_LIST = "Представляю Вашему вниманию перечень услуг компании Ростелеком:"
    RT_CLEVER_HOUSE_START = "Набор устройств стройств умного дома:"
    RT_CLEVER_HOUSE_MORE = "Если желаете, могу рассказать поподробнее про любое из данных устройств"
    NICE_TO_MEET_YOU = "Приятно познакомиться!"
    PRINT_YOUR_REQUESR = "Введите текст Вашего обращения:"
    WOULD_YOU_LIKE_TO_SEE_IT = "Хотите посмотреть, как он выглядит? (да/нет)"
    OK = "Хорошо! "
    ANY_MORE_DEVICES = "Не желаете посмотреть про ещё какие-нибудь девайсы?"
    DONT_UNDERSTAND = "Я боюсь, что не могу Вас понять, давайте ещё раз попробуем!"