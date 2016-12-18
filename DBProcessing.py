# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Взаимодействие с базой данных
# Автор: Ракитин Виталий
#
# База данных пользователей Users:
# +-----------+------------+-----------+--------------+
# | user_id   | first_name | last_name | phone_number |
# +-----------+------------+-----------+--------------+
#
# База данных запросов пользователей Notifications:
# +-----------+-----------------------------------+---------------------+
# | user_id   | notification                      | date                |
# +-----------+-----------------------------------+---------------------+

from MySQL import *

def create_new_user(message): 
    ''' 
    Create New User in DB 
    ''' 
    table = "Users"
    args = (message["user_id"],message["first_name"],message["last_name"],message["phone_number"])  
    form = "%s"
    for i in xrange(len(args)-1):
        form += ",%s"
    insert_into(table,form, args)


def create_user_dict_from_db_answer(answer):
    ''' 
    answer list from Users to dict 
    '''
    res = {}
    res["user_id"] = answer[0].encode("utf-8")
    res["first_name"] =  answer[1].encode("utf-8")
    res["last_name"] =  answer[2].encode("utf-8")
    res["phone_number"] =  answer[3].encode("utf-8")
    return res


def check_user_in_users_db(uid):
    '''
    Check if user already exists in DB and get his contact
    '''
    info = select_from_where("*","users","user_id",uid)
    if len(info):
        return True, info[0]
    return False, None

def send_task_from_helper(message):
    ''' 
    Отправляется вопрос пользователя в базу данных notifications,
    Если бот не может на него ответить
    '''
    table = "Notifications"
    args = (message["user_id"],message["notification"],message["date"])  
    form = "%s"
    for i in xrange(len(args)-1):
        form += ",%s"
    insert_into(table,form, args)

if __name__ == "__main__":
    drop_table("Users")
    create_table("users",["user_id","first_name","last_name","phone_number"],["char(32)","char(255)","char(255)","char(32)"] )
    demo_user1 = {"user_id" : "000001", "first_name": "Винни", "last_name": "Пух", "phone_number":"+12" }
    demo_user2 = {"user_id" : "000002", "first_name": "Кристофер", "last_name": "Робинс", "phone_number":"+725" }
    create_new_user(demo_user1)
    print is_user_in_users(demo_user1)
    print is_user_in_users(demo_user2)