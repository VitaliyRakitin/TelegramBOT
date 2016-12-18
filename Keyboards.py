# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Клавиатуры
# Автор: Ракитин Виталий
#

from telegram import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup

send_contact_keyboard =  ReplyKeyboardMarkup([[KeyboardButton("Представиться",request_contact = True)]], one_time_keyboard=True)

RT_SERVICES_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text = "Интернет",callback_data="internet")],
                                        [InlineKeyboardButton(text = "Умный дом",callback_data="home")],
                                        [InlineKeyboardButton(text = "Техподдержка",callback_data="help")]])

CleverHouse_keyboard = ReplyKeyboardMarkup([["1","2","3"],["4","5","6"],["7"]], one_time_keyboard=True)

YES_NO_keyboard = ReplyKeyboardMarkup([["да","нет"]], one_time_keyboard=True)