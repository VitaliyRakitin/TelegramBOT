#!/usr/bin/python 
# -*- coding: utf-8 -*-
#
# Телеграм Бот 
# Приведение слова к правильному виду
# Автор: Ракитин Виталий
#
# http://polyglot.readthedocs.io/en/latest/Installation.html !!!
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
        Перебор всех соседей слов.
        deletion --- remove one letter 
        transposition --- swap two adjacent letters,
        replacement --- change one letter to another 
        insertion --- add a letter
        returns a set of all the edited strings (whether words or not) that can be made with one simple edit
        '''
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)] # куски
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

        check = self.allwords.check_word(word.encode("utf-8"))
        if check:
            return check

        edits_words = self.edits(word)
        for w in edits_words:
            check = self.allwords.check_word(w.encode("utf-8"))
            if check:
                return check
        return word

    def stemming(self, word):
        return self.stemmer.stemWord(word)

if __name__ == "__main__":
    correction = WordCorrection()
    print correction.spell_correction("Устроство")