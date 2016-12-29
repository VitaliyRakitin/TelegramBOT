#!/usr/bin/python 
# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Клавиатуры
# Автор: Ракитин Виталий
#

from telegram import (KeyboardButton,
                      ReplyKeyboardMarkup,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup)


class Keyboards():
    SEND_CONTACT_KEYBOARD = ReplyKeyboardMarkup(
                                [[KeyboardButton("Представиться",
                                                 request_contact = True)]], 
                                one_time_keyboard=True)

    CLEVER_HOUSE_KEYBOARD = ReplyKeyboardMarkup(
                                [["1","2","3"],["4","5","6"],["7"]], 
                                one_time_keyboard=True)

    YES_NO_KEYBOARD = ReplyKeyboardMarkup(
                                [["да","нет"]], 
                                one_time_keyboard=True)

    RT_SERVICES_KEYBOARD = InlineKeyboardMarkup(
                                [[InlineKeyboardButton(text = "Интернет",
                                                       callback_data="internet")],
                                [InlineKeyboardButton(text = "Умный дом",
                                                      callback_data="home")],
                                [InlineKeyboardButton(text = "Техподдержка",
                                                      callback_data="help")]])