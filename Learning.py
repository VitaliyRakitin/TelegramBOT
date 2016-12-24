#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Поиск наиболее подходящего ответа на  запрос пользователя
# Автор: Ракитин Виталий
#


from DB import  QuestionsDB
from Tokenizer import Tokenizer
import numpy as np

class Learning(object):
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.qusetions_db = QuestionsDB()
        self.training_words = []
        self.training_matrix = np.array([])
        self.NO_SUCH_ANSWER = -1

    def fit(self):
        '''
        Создаём обучающую модель
        '''
        questions = self.qusetions_db.get_questions() # array of tuples (number, question)

        
        training_sentances = []
        for number,question in questions:
            tokens = self.tokenizer.get_text_tokens(question.encode("utf-8"))
            training_sentances.append(tokens)
            for word in tokens:
                if word not in self.training_words:
                    self.training_words.append(word)

        self.training_matrix = self.create_matrix(training_sentances)      
        return self

    def create_matrix(self, training_sentances):
        '''
        Создаём обучающую матрицу
        '''
        matrix = []
        for sentence in training_sentances:
            new_line = []
            for word in self.training_words:
                if word in sentence:
                    new_line.append(1)
                else:
                    new_line.append(0)
            matrix.append(new_line)
        return np.array(matrix) 

    def create_prediction_vector(self, tokens):
        '''
        Создаём обучающий вектор для нашего запроса
        '''
        if len(tokens) == 0:
            tokens.append("")
        return self.create_matrix(tokens)[0]
        
    def predict(self, question):
        tokens = self.tokenizer.get_text_tokens(question)
        predict_vector = self.create_prediction_vector(tokens)
        result_vector = np.dot(self.training_matrix, predict_vector)
        if result_vector.max() != 0:   
            number = np.argmax(result_vector)
            return self.qusetions_db.get_answer(number)
        else: 
            return self.NO_SUCH_ANSWER


if __name__ == "__main__":
    model = Learning()
    model.fit()
    res = model.predict("Лама не грит и врут календари!")
    if res == -1:
        print "No such word"
    else:
        print res