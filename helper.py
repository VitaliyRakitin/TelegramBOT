# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Техподдержка
# Автор: Ракитин Виталий
#
# Искуственный интеллект распознавания запросов.
# Если бот не может ответить на вопрос, то он сохраняется в базе данных.
#
# База данных запросов пользователей Notifications:
# +-----------+-----------------+---------------------+
# | user_id   | notification    | date                |
# +-----------+-----------------+---------------------+
#
# База данны для хранения всех слов (для проверки корректности)
# +-------------+-----------+
# | words       | frequency |
# +-------------+-----------+
#
# База данных для хранения стоп-слов
# +----------------------------+
# | stopwords                  |
# +----------------------------+


#import nltk
#import string
#from nltk.corpus import stopwords

#stop_words = stopwords.words('russian')
#drop_table("stopwords")
#create_table("stopwords",["stopwords"],["char(255)"])
#for i in stop_words:
#	insert_into("stopwords","%s",(i,));

from MySQL import *
from constants import *
from DBProcessing import send_task_from_helper
import Stemmer
import re
from collections import defaultdict
import numpy as np
from Keyboards import RT_SERVICES_keyboard

stemmer = Stemmer.Stemmer('russian')
alphabet = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'



def get_words(text):
    '''
    returns list of words
    '''
    words = []
    blocks = [block for block in text.split(" ") if block != ''] 
    for block in blocks:
        words.append("".join(re.findall(u'[а-яА-Я]', block.decode('utf8'))))
    return words

def get_stop_words():
    '''
    Скачаем стоп-слова из базы данных
    '''
    words = select_from("*","stopwords")
    return [word[0] for word in words]

def get_tokens(words):
    '''
    приевдём к нижнему регистру 
    и отберём список всех токенов
    '''
    stops =  get_stop_words()
    new_words = []
    for word in words:
        word = word.lower()
        #print word        #print word
        if word not in stops and len(word) > 1:
            #word = stemmer.stemWord(word)
            new_words.append(word)
    return new_words

def get_text_tokens(text):
    ''' 
    отберём токены 
    '''
    #text = unicode(text.encode("utf-8"),"utf-8").encode("utf-8").lower() 
    return get_tokens(get_words(text))

def edits(word):
    '''
    Перебор всех соседей слов
    '''
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return list(set(deletes + transposes + replaces + inserts))


def spell_correction(word):
    '''
    Исправление описок и ошибок в словах методом перебора соседей
    '''
    if not isinstance(word, unicode):
        word = word.decode("utf-8")
    word = word.lower()
    edits_words = edits(word)
    for w in edits_words:
        check_list = select_from_where("words","allwords","words",w.encode("utf-8"))
        if len(check_list):
            return w
    return word

#special_stops = ["могу", "устройство"]

def stemming(word):
    return stemmer.stemWord(word)

def create_study_matrix(all_sentences, all_study_words):
    '''
    Создаём обучающую матрицу
    '''
    matrix = []
    for sentence in all_sentences:
        new_line = []
        for word in all_study_words:
            if word in sentence:
                new_line.append(1)
            else:
                new_line.append(0)
        matrix.append(new_line)
    return matrix

def create_message_study_lits(message, all_study_words):
    '''
    Создаём обучающий вектор для нашего запроса
    '''
    words = get_text_tokens(message)
    for i,word in enumerate(words):
        if word not in all_study_words:
            words[i] = spell_correction(word)
    return create_study_matrix([words], all_study_words)[0]

def create_study_words_list():
    '''
    Создаём списки всех обучающих слов и предложений
    '''
    all_sentences = []
    all_study_words = []
    for i,text in enumerate(QUESTIONS):
        study_tokens = get_text_tokens(text)
        all_sentences.append(study_tokens)
        for word in study_tokens:
            if word not in all_study_words:
                all_study_words.append(word)
    return all_sentences, all_study_words


def predict_answer(message,all_study_words,study_matrix):  
    '''
    Подберём наиболее подходящий ответ по запросу
    '''  
    message_list = create_message_study_lits(message,all_study_words)
    result_vector = np.dot(study_matrix,message_list)
    print result_vector
    if result_vector.max() != 0:   
        return np.argmax(result_vector)
    else: 
        return NO_SUCH_ANSWER


#for i in study_words:
#    p = stemming(spell_correction(i))


all_sentences, all_study_words = create_study_words_list()
study_matrix = np.array(create_study_matrix(all_sentences, all_study_words))



def create_notification(message):
    '''
    Из стандартного типа message создаём notification,
    чтобы внести запрос в базу
    '''
    notification = {}
    notification["user_id"] = message.from_user.id
    notification["notification"] = message.text
    notification["date"] = message.date
    return notification


def helper(bot,update):
    '''
    собственно помошник
    '''
    text = update.message.text
    text = unicode(text.encode("utf-8"),"utf-8").encode("utf-8").lower() 
    answer_index = predict_answer(text,all_study_words,study_matrix)
    if answer_index == NO_SUCH_ANSWER:
        send_task_from_helper(create_notification(update.message))
        update.message.reply_text("Извините, к сожалению, я не могу сейчас ответить на Ваш вопрос! Он уже передан в техподдержку! Вам обязательно перезвонят!")
    else:
        update.message.reply_text(QUESTIONS[answer_index])
        update.message.reply_text(ANSWERS[answer_index])

    update.message.reply_text(RT_SERVICES,reply_markup = RT_SERVICES_keyboard)
    return START_CONVERSATION


if __name__ == "__main__":
    message1 = "Грустняшка" # такого слова нет в наличии 
    message2 = "Не работает устроство! Прпадает! Что делать?" #специально с ошибками, другое предложение

    predict_answer(message1,all_study_words,study_matrix)
    predict_answer(message2,all_study_words,study_matrix)


#check_word = "Саша"
#print check_word,spell_correction(check_word)
#for i in res:
#   insert_into("allwords","%s,%s",(i,res[i]));

