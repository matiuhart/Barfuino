#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Libreria de consultas a base de datos
'''
import MySQLdb
import MySQLdb.cursors


# VARIABLES PARA CONEXION DE DB
DB_HOST = '192.168.0.10'
DB_USER = 'barfuino'
DB_PASS = '114529'
DB_NAME = 'barfuino'


class MysqlQuery(object):
    query = ''
    connString = [DB_HOST, DB_USER, DB_PASS, DB_NAME]

    def __init__(self,query=''):
        self.query = query
        MysqlQuery.query = self.query

    # Consulta basica devuelta en una tupla
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

    # Consulta tipo diccionario para devolver un registro especifico
    def runQueryAsDictOne(self):
    	db = MySQLdb.connect(*MysqlQuery.connString,cursorclass=MySQLdb.cursors.DictCursor)
    	cursor = db.cursor()
    	cursor.execute(MysqlQuery.query)

        if MysqlQuery.query.upper().startswith('SELECT'):
            datosConsulta = cursor.fetchone()

        else:
            db.commit()
            datosConsulta = None

        cursor.close()
        db.close()

    	return datosConsulta

    # Consulta tipo diccionario para devolver todos los valores en un diccionario
    def runQueryAsDictAll(self):
        db = MySQLdb.connect(*MysqlQuery.connString,cursorclass=MySQLdb.cursors.DictCursor)
        cursor = db.cursor()
        cursor.execute(MysqlQuery.query)

        if MysqlQuery.query.upper().startswith('SELECT'):
            datosConsulta = cursor.fetchall()

        else:
            db.commit()
            datosConsulta = None

        cursor.close()
        db.close()

        return datosConsulta





'''
EJEMPLO PARA DEVOLVER TODOS LOS REGISTROS COMO DICCIONARIO

qry="SELECT id,f_fermentador FROM t_produccionestados WHERE f_activa = 'T'"
conexion = MysqlQuery(qry)
resultado = conexion.runQueryAsDictAll()

# Recupero valores
for row in resultado:
    datos = [row['id'],row['f_fermentador']]
    print datos

Ó

datos = resultado[0]

id = datos['id']
'''


