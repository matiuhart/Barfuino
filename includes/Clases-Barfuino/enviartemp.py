#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import MySQLdb
#import MySQLdb.cursors
from dbconn import *
from seriecom import *


db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="114529", db="barfuino",cursorclass=MySQLdb.cursors.DictCursor)
cursor = db.cursor()

# Clase para comprobacion de fase actual
class ArduinoQuery(object):
    fase = 0
    def __init__(self,numeroFermentador = '',temperatura = ''):
        self.fermentador = numeroFermentador
        self.temperatura = temperatura

    # Devuelve temperatura seteada para numeroFermentador x
    def QueryTemperaturaSeteada(self):
        serial_w('f',ArduinoQuery.fermentador)

    # Devuelve la temperatura actual para numeroFermentador x
    def QueryTepmperaturaActual(self):
        serial_w('g',ArduinoQuery.fermentador)
        time.sleep(2.5)
        print(temperatura)


    # Watchdog para verificar estado de arduino
    def QueryEstadoArduino(self):
        serial_w('hi')

    # Setea temperatura para numeroFermentador x
    def QuerySeteoTemperatura(self):
        serial_w('s',ArduinoQuery.fermentador,ArduinoQuery.temperatura)


'''
def QueryTepmperaturaActual(mode,fermentador):
        serial_w('g',fermentador)
        time.sleep(2.5)
        print(temperatura)
'''