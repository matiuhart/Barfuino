import MySQLdb
import MySQLdb.cursors
#import os
#import time
#from datetime import datetime, timedelta

# VARIABLES PARA CONEXION DE DB
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = '114529'
DB_NAME = 'barfuino'


class MysqlQuery(object):
    query = ''
    connString = [DB_HOST, DB_USER, DB_PASS, DB_NAME]

    def __init__(self,query=''):
        self.query = query
        MysqlQuery.query = self.query

    def runQueryAsBasic(self):
        db = MySQLdb.connect(*MysqlQuery.connString)
        cursor = db.cursor()
        cursor.execute(MysqlQuery.query)

        if MysqlQuery.query.upper().startswith('SELECT'):
            datosConsulta = cursor.fetchall()

        else:
            conn.commit()
            datosConsulta = None

        cursor.close()
        db.close()

        return datosConsulta

    def runQueryAsDictOne(self):
    	db = MySQLdb.connect(*MysqlQuery.connString,cursorclass=MySQLdb.cursors.DictCursor)
    	cursor = db.cursor()
    	cursor.execute(MysqlQuery.query)

        if MysqlQuery.query.upper().startswith('SELECT'):
            datosConsulta = datosConsulta=cursor.fetchone()

        else:
            db.commit()
            datosConsulta = None

        cursor.close()
        db.close()

    	return datosConsulta

    def runQueryAsDictAll(self):
        db = MySQLdb.connect(*MysqlQuery.connString,cursorclass=MySQLdb.cursors.DictCursor)
        cursor = db.cursor()
        cursor.execute(MysqlQuery.query)

        if MysqlQuery.query.upper().startswith('SELECT'):
            datosConsulta = datosConsulta=cursor.fetchall()

        else:
            db.commit()
            datosConsulta = None

        cursor.close()
        db.close()

        return datosConsulta



