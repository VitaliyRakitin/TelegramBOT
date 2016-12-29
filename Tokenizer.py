#!/usr/bin/python 
# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Токенизация слов
# Автор: Ракитин Виталий
#

import re

from WordCorrection import WordCorrection
from DB import  StopWordsDB



class Tokenizer(object):

    def __init__(self):
        self.correct = WordCorrection()
        self.stops = StopWordsDB().get_stops()

    def get_words(self, text):
        '''
        returns list of words
        '''
        words = []
        blocks = [block for block in text.split(" ") if block != ''] 
        for block in blocks:
            words.append("".join(re.findall(u'[а-яА-Я]', block.decode('utf8'))))
        return words

    def get_tokens(self, words):
        '''
        и отберём список всех токенов
        '''
        new_words = []
        for word in words:
            if word not in self.stops and len(word) > 1:
                word = self.correct.spell_correction(word)
                new_words.append(word)
        return new_words

    def get_text_tokens(self, text):
        return self.get_tokens(self.get_words(text))


if __name__ == "__main__":
    tokenizer = Tokenizer()
    for i in tokenizer.get_text_tokens("Устроство плох работат!"):
        print i