#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Приведение слова к правильному виду
# Автор: Ракитин Виталий
#

import Stemmer
from DB import AllWordsDB


class WordCorrection(object):
    def __init__(self):
        self.alphabet = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.allwords = AllWordsDB()
        self.stemmer = Stemmer.Stemmer('russian')

    def edits(self, word):
        '''
        Перебор всех соседей слов
        '''
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
        inserts    = [a + c + b     for a, b in splits for c in self.alphabet]
        return list(set(deletes + transposes + replaces + inserts))

    def spell_correction(self, word):
        '''
        Исправление описок и ошибок в словах методом перебора соседей
        '''
        if not isinstance(word, unicode):
            word = word.decode("utf-8")

        word = word.lower()

        if self.allwords.check_word(word.encode("utf-8")):
            return word

        edits_words = self.edits(word)
        for w in edits_words:
            if self.allwords.check_word(w.encode("utf-8")):
                return w
        return word

    def stemming(self, word):
        return self.stemmer.stemWord(word)

if __name__ == "__main__":
    correction = WordCorrection()
    print correction.spell_correction("Устроство")