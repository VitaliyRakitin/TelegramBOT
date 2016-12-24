#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Телеграм Бот компании Ростелеком
# Обработка запросов к MySQL серверу
# Автор: Ракитин Виталий
#

import mysql.connector as sql
from config import MYSQL_CONFIG

class MySQL():
    def __init__(self):
        self.config = MYSQL_CONFIG

    def select_from(self, select, table, add = ""):
        result = [] 
        select_string = ""
        for word in select:
            if len(select_string) > 0:
                select_string += ','
            select_string += word

        query = "SELECT {0} FROM {1} {2}".format(select_string, table, add) 
        try:  
            connect = sql.MySQLConnection(**self.config) 
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


    def select_from_where(self, select, table, where_what, where_to):
        query = 'WHERE {0} = "{1}"'.format(where_what, where_to)
        return self.select_from(select, table, query)

     
    def send_request(self, request,args = None):
        '''Requests without an answer'''
        try: 
            connect = sql.MySQLConnection(**self.config) 
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


    def drop_table(self, tablename):
        ''' Delete table '''
        query = "DROP TABLE IF EXISTS {0}".format(tablename)
        self.send_request(query)


    def create_table(self, tablename, columns=[] ,types=[]):
        query_columns = ""
        for i,column in enumerate(columns):
            if len(query_columns) > 0:
                query_columns += ','
            query_columns += "{0} {1}".format(column,types[i])

        query = "CREATE TABLE {0}".format(tablename)
        if len(query_columns) > 0:
            query +=  "({0})".format(query_columns)

        self.send_request(query)


    def insert_into(self, table, form, args):
        query = "INSERT INTO {0} VALUES({1})".format(table,form) 
        self.send_request(query,args)

#def update(table)

if __name__ == "__main__":
    pass 