# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Обработка запросов к MySQL серверу
# Автор: Ракитин Виталий
#

import mysql.connector as sql
from config import MYSQL_CONFIG

config = MYSQL_CONFIG

def select_from(select, table, add = ""):
    result = [] 
    query = "SELECT {0} FROM {1} {2}".format(select, table, add) 
    try:  
        connect = sql.MySQLConnection(**config) 
        if connect.is_connected(): 
            cursor = connect.cursor() 
            cursor.execute(query)     
            row = cursor.fetchone()
 
            while row is not None: 
                result.append(row) 
                row = cursor.fetchone()
 
            cursor.close() 
            connect.close()
 
        else: 
            print "Connection error"
 
    except sql.Error as error: 
            print error 
    return result


def select_from_where(select, table, where_what, where_to):
    query = 'WHERE {0} = "{1}"'.format(where_what,where_to)
    return select_from(select, table, query)

     
def send_request(request,args = None):
    '''Requests without an answer'''
    print request
    try: 
        connect = sql.MySQLConnection(**config) 
        if connect.is_connected(): 
            cursor = connect.cursor() 
            if args:
                cursor.execute(request,args)
            else:
                 cursor.execute(request)
            connect.commit() 
     
            cursor.close() 
            connect.close() 
        else: 
            print "Connection error" 
     
    except sql.Error as error: 
        print error 


def drop_table(tablename):
    ''' Delete table '''
    query = "DROP TABLE IF EXISTS {0}".format(tablename)
    send_request(query)


def create_table(tablename,columns=[],types=[]):
    query_columns = ""
    for i,column in enumerate(columns):
        if len(query_columns) > 0:
            query_columns += ','
        query_columns += "{0} {1}".format(column,types[i])

    query = "CREATE TABLE {0}".format(tablename)
    if len(query_columns) > 0:
        query +=  "({0})".format(query_columns)
    send_request(query)


def insert_into(table,form,args):
    query = "INSERT INTO {0} VALUES({1})".format(table,form) 
    send_request(query,args)

#def update(table)

if __name__ == "__main__":
    pass