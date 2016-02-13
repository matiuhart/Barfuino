##!/usr/bin/python
# -*- encoding: utf-8 -*-

'''
Clases para operaciones con fechas y horas
'''

import datetime
from datetime import timedelta



# FUNCION PARA SUMA DE DIAS
def SumarDias(dias=0):
    fecha = datetime.datetime.now() + datetime.timedelta(days=dias)
    nuevaFecha = fecha.strftime("%Y-%m-%d %H:%M:%S")
    return nuevaFecha

# FUNCION PARA RESTA DE DIAS
def RestarMinutos(minutos=0):
    hora = datetime.datetime.now() - datetime.timedelta(minutes=minutos)
    nuevaHora = hora.strftime("%Y-%m-%d %H:%M:%S")
    return nuevaHora
