#!/usr/bin/python 
# -*- coding: utf-8 -*-
#
# Телеграм Бот 
# Взаимодействие с базами данных
# Автор: Ракитин Виталий
#
# UserDB, NotificationDB
#

from MySQL import MySQL
from datetime import datetime

class UsersDB(object):
    '''
    Обработка базы данных пользователей Users
    +-----------+------------+-----------+--------------+
    | user_id   | first_name | last_name | phone_number |
    +-----------+------------+-----------+--------------+
    '''

    def __init__(self):
        self.TABLE = "USERS"
        self.UID = "user_id"
        self.FIRST_NAME = "first_name"
        self.LAST_NAME = "last_name"
        self.NUMBER = "phone_number"
        self.ALL = "*"
        self.COUNT = "COUNT(*)"
        
        self.sql = MySQL()

    def create_new_user(self, userinfo): 
        ''' 
        Create New User in DB.
        userinfo = dict()
        ''' 
        args = (userinfo[self.UID],
                userinfo[self.FIRST_NAME],
                userinfo[self.LAST_NAME],
                userinfo[self.NUMBER])  
        
        string_format = "%s"
        for i in xrange(len(args)-1):
            string_format += ",%s"

        self.sql.insert_into(self.TABLE, string_format, args)


    def check_user_in_db(self, uid):
        '''
        Check if user already exists in DB and get his contact
        ''' 
        info = self.sql.select_from_where([self.ALL], self.TABLE, self.UID, uid)
        if len(info):
            return True, info[0]
        return False, None


    def create_user_dict_from_db_answer(self, answer):
        ''' 
        answer list from Users to dict 
        '''
        res = {}
        res[self.UID] = answer[0].encode("utf-8")
        res[self.FIRST_NAME] =  answer[1].encode("utf-8")
        res[self.LAST_NAME] =  answer[2].encode("utf-8")
        res[self.NUMBER] =  answer[3].encode("utf-8")
        return res


#-------------------------------------------------------#
class NotificationsDB(object):
    '''
    Обработка базы данных запросов Notifications:
    +-----------+----------------+---------+
    | user_id   | notification   | date    |
    +-----------+----------------+---------+
    '''

    def __init__(self):
        self.TABLE = "Notifications"
        self.UID = "user_id"
        self.NTF = "notification"
        self.DATE = "date"
        
        self.sql = MySQL()

    def send_notification(self, notification):
        ''' 
        Отправляется вопрос пользователя в базу данных notifications,
        Если бот не может на него ответить
        '''
        args = (notification[self.UID],
                notification[self.NTF],
                notification[self.DATE])  

        string_format = "%s"
        for i in xrange(len(args)-1):
            string_format += ",%s"

        self.sql.insert_into(self.TABLE, string_format, args)


#-------------------------------------------------------#
class StopWordsDB(object):
    '''
    Обработка базы данных хранения стоп-слов
    +----------------------------+
    | stopwords                  |
    +----------------------------+
    '''
    def __init__(self):
        self.TABLE = "stopwords"
        self.ALL = "*"
        self.COUNT = "COUNT(*)"
        self.sql = MySQL()

    def get_stops(self):
        words = self.sql.select_from([self.ALL],self.TABLE)
        return [word[0] for word in words]    


#-------------------------------------------------------#
class AllWordsDB(object):
    '''
    Обработка базы данных хранения всех слов (для проверки корректности)
    +----------+-----------+-----------+
    | words    | synonym   | frequency |
    +----------+-----------+-----------+
    '''
    def __init__(self):
        self.TABLE = "allwords"
        self.COLUMN = "words"
        self.SYNONYM = "synonym"
        self.COUNT = "COUNT(*)"
        self.sql = MySQL()

    def check_word(self,word):
        '''Returns the best synonym of the word'''
        res_list = self.sql.select_from_where([self.SYNONYM],
                                              self.TABLE,
                                              self.COLUMN,
                                              word)
        if len(res_list) > 0:
            return res_list[0][0]
        else:
            return False

#-------------------------------------------------------#
class QuestionsDB(object):
    '''
    Обработка базы данных хранения вопросов и ответов техподдержки Question:
    +----------+------------+---------+
    | number   | question   | answer  |
    +----------+------------+---------+
    '''
    def __init__(self):
        self.TABLE = "questions"
        self.QUESTION = "question"
        self.ANSWER = "answer"
        self.NUMBER = "number"
        self.ALL = "*"
        self.COUNT = "COUNT(*)"
        self.sql = MySQL()

    def get_questions(self):
        questions = self.sql.select_from([self.NUMBER,self.QUESTION],self.TABLE)
        questions.sort(key = lambda item: item[0]) # sort by number 
        return questions
    def get_answer(self, number):
        answer = self.sql.select_from_where([self.QUESTION, self.ANSWER],self.TABLE,self.NUMBER,number)
        return answer[0]

    def add_question(self, question, answer, number = None):
        if number == None:
            questions = self.sql.select_from([self.COUNT],self.TABLE)
            number = questions[0][0]

        args = (number, question, answer)
        
        string_format = "%s"
        for i in xrange(len(args)-1):
            string_format += ",%s"

        self.sql.insert_into(self.TABLE, string_format, args)

#-------------------------------------------------------#
class DevicesDB(object):
    '''
    Обработка базы данных хранения устройств умного дома, 
    их описаний,соответствующего Emoji 
    и путь, откуда можно взять файл изображения:
    +----------+--------+--------------+--------+--------+
    | number   | name   | description  | path   |
    +----------+--------+--------------+--------+--------+
    '''
    def __init__(self):
        self.TABLE = "devices"
        self.NAME = "name"
        self.DESCR = "description"
        #self.EM = "emoji"
        self.PATH = "path"
        self.NUMBER = "number"
        self.ALL = "*"        
        self.COUNT = "COUNT(*)"
        self.sql = MySQL()

    def add_device(self, name, description, path,number = None):
        if number == None:
            questions = self.sql.select_from([self.COUNTALL],self.TABLE)
            number = questions[0][0]

        args = (number, name, description, path)
        
        string_format = "%s"
        for i in xrange(len(args)-1):
            string_format += ",%s"

        self.sql.insert_into(self.TABLE, string_format, args)

    def get_devices(self):
        devices = self.sql.select_from([self.NUMBER,self.NAME],self.TABLE)
        devices.sort(key = lambda item: item[0]) #sort by number
        return devices

    def get_description(self, number):
        description = self.sql.select_from_where([self.NAME,self.DESCR], self.TABLE, self.NUMBER, number)
        return description[0]
   
    def get_img_path(self, number):
        path = self.sql.select_from_where([self.PATH],self.TABLE,self.NUMBER, number)
        return path[0][0]   


if __name__ == "__main__":
    pass
#    db = UsersDB()
#    demo_user1 = {"user_id" : "000001", "first_name": "Винни", "last_name": "Пух", "phone_number":"+12" }
#    demo_user2 = {"user_id" : "000002", "first_name": "Кристофер", "last_name": "Робинс", "phone_number":"+725" }
#    db1 = NotificationsDB()
#    notification = {"user_id" : "000001", "notification": "Check! Проверка!", "date" : datetime.utcnow()}
#    db1.send_notification(notification)
#    print db.check_user_in_db(demo_user1["user_id"])
#    print db.check_user_in_db(demo_user2["user_id"])

#    QUESTIONS = [
#    "Не могу зарегистрировать контроллер",
#    "Не могу добавить устройство.",
#    "Не могу удалить устройство.",
#    "Ложные срабатывания датчика протечки",
#    "Если датчик не работает",
#    "Если умная лампа не добавляется в сеть",
#    "Устройство иногда пропадает и не срабатывает.",
#    "Если устройство определилось неправильно"
#    ]

#    ANSWERS = [
#    "1. Проверьте, тот ли MAC-адрес Вы вводите? У контроллера есть 2 MAC-адреса – Wi-Fi MAC  и LAN MAC. Вам требуется вводить LAN MAC.\n2. Проверьте, подключен ли контроллер проводом в локальную сеть, если используется проводное подключение. Проверьте, подключен ли контроллер в вашу Wi-Fi сеть, если используется подключение через WPS",
#    "1. Проверьте, удалена ли с датчика защитная этикетка\n2. Попробуйте поднести устройство поближе к контроллеру\n3. Попробуйте заменить батарейку в устройстве",
#    "Нажмите кнопку «удалить» в интерфейсе устройства. Подождите некоторое время, и оно удалится из интерфейса.",
#    "Проверьте, не замыкаются ли его контакты чем-то металлическим, например, трубой.",
#    "проверьте, правильно ли установлены батарейки и наличие заряда батареек",
#    "постучите немного сильнее  по лампе.",
#    "1. Скорее всего, проблема в том, что контроллер не может связаться с устройством. Попробуйте поднести его поближе и протестировать на срабатывание. Если это действие помогло – поставьте между устройством и контроллером розетку или лампу – они будут ретранслировать сигнал.\n2. Если уже прошло много времени, возможно, у устройства села батарейка. Рекомендуется проверить уровень заряда устройства, и при необходимости заменить ее.",
#    "Попробуйте удалить устройство, и заново добавить его в контроллер. Возможно, что первоначально оно неправильно прошло регистрацию в контроллере."
#    ]

#    qdb = QuestionsDB()
#    for i,question in enumerate(QUESTIONS):
#        qdb.add_question(question,ANSWERS[i])

#    print qdb.get_questions()
#    print qdb.get_answer(1)

 #   from telegram.emoji import Emoji as em

#    RT_CLEVER_HOUSE_DEVICES = [
#    "Контроллер  умного дома",
#    "Датчик движения",
#    "Датчик открытия",
#    "Датчик протечки",
#    "Датчик дыма",
#    "Умная розетка",
#    "Умная лампочка"    
#    ]

#    DEVICES_EMOJI = [
#    unicode(em.MOBILE_PHONE),
#    unicode(em.RUNNER),
#    unicode(em.CLOSED_LOCK_WITH_KEY),
#    unicode(em.POTABLE_WATER_SYMBOL),
#    unicode(em.FIRE),
#    unicode(em.ELECTRIC_PLUG),
#    unicode(em.ELECTRIC_LIGHT_BULB)
#    ]

 #   RT_CLEVER_HOUSE_DEVICES_TEXT =[
 #   "Контроллер умного дома управляет устройствами, настраивает систему умного дома, позволяет создавать сценарии, дает удаленный доступ к умному дому и организует работу с помощью приложения.  Контроллер может взаимодействовать одновременно с 230 устройствами Z-Wave и оснащен резервным питанием, так что при потере питания в течении двух часов он мог сообщить о проблеме на телефон пользователю (при наличии интернета).",
 #   "Датчик движения реагирует на движение и сочетает в себе датчики движения, температуры и освещенности. Идеален для управления световыми  и охранными сценариями.\nНа страже безопасности вашего дома.",
 #   "Датчик открытия диагностирует открытие двери/окна и сочетает в себе датчики температуры и освещенности. Идеален для управления световыми  и охранными сценариями.\nНа страже безопасности вашего дома.",
 #   "Датчик протечки реагирует в случае протечки и сочетает в себе датчики температуры и влажности. Удобная конструкция датчика позволяет установить в любом, даже самом труднодоступном месте, что помогает обнаружить протечку на ранней стадии.\nРано обнаружить - быстро предотвратить",
 #   "Датчик дыма в случае задымления оповестит о возникшей проблеме звуковым сигналом, push уведомлением и сообщением на телефон. Идеален для работы в сценариях безопасности умного дома.\nДоверить безопасность вашего дома профессионалам.",
 #   "Умная розетка включает/выключает торшеры и ночники или электрические приборы с пультов управления, со смартфона или с помощью удаленного доступа. Идеальна в сценариях управления умным светом и отоплением.\nВы всегда сможете отключить забытый утюг, а, засыпая, легко выключить лампу в дальнем конце комнате.",
 #   "Умная лампочка динамично подстраивается под настроение с помощью 16 млн. цветов. Идеальна для использования в сценариях или управления подсветкой помещения с помощью приложения.\nПодстроить свой дом под сегодняшнее настроение."
 #   ]

 #   RT_CLEVER_HOUSE_DEVICES_PATH = [
 #   "house/1.png",
 #   "house/2.png",
 #   "house/3.png",
 #   "house/4.png",
 #   "house/5.png",
 #   "house/6.png",
 #   "house/7.jpg",
 #   ]   

 #   db = DevicesDB()
 #   for i,dev in enumerate(RT_CLEVER_HOUSE_DEVICES):
 #       db.add_device(dev,RT_CLEVER_HOUSE_DEVICES_TEXT[i],RT_CLEVER_HOUSE_DEVICES_PATH[i])
 #   print db.get_devices()    
