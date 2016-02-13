#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Este modulo realiza la comprobacion de fase actual del fermentador. Verifica la cantidad de dias de cada fase y reliza el cambio de si es necesario, actualizando el
valor de temperatura sobre arduino y su respectivo campo f_produccionfasesid en la tabla t_produccionestados.
'''

import MySQLdb
import MySQLdb.cursors
import datetime
from dbconn import *
from seriecom import *
from notificaciones import *
from estadoarduino import *

db = MySQLdb.connect(host="192.168.0.10", port=3306, user="barfuino", passwd="114529", db="barfuino",cursorclass=MySQLdb.cursors.DictCursor)
cursor = db.cursor()

# Clase para comprobacion de fase actual
class ComprobarFase(object):
    fase = 0
    def __init__(self,produccionEstadoId):
        self.estadoId=produccionEstadoId

        cursor.execute('SELECT t_produccionfases.id, t_produccionfases.f_nombre FROM t_produccionestados JOIN t_produccionfases ON t_produccionestados.f_produccionfasesid = t_produccionfases.id WHERE t_produccionestados.id =%s' %(self.estadoId))
        datosConsulta=cursor.fetchone()

        ComprobarFase.fase = datosConsulta['f_nombre']

    def faseActual(self):
        if (ComprobarFase.fase == 1):
            return 1
        elif (ComprobarFase.fase == 2):
            return 2
        elif (ComprobarFase.fase == 3):
            return 3
        elif (ComprobarFase.fase == 4):
            return 4
        elif (ComprobarFase.fase == 5):
            return 5
        else:
            return 6
#CONSULTAS
'''
SELECT t_produccionfases.id, t_produccionfases.f_nombre FROM t_produccionestados JOIN t_produccionfases ON t_produccionestados.f_produccionfasesid = t_produccionfases.id WHERE t_produccionestados.id ='14'
'''
##### CLASE DE CAMBIO
class CambiarFase(object):
    ahora = datetime.datetime.now()
    finFase = ''
    estadoId = 0
    fermentador = 0
    temperaturas = ''

    def __init__(self,produccionEstadoId):
        CambiarFase.estadoId = produccionEstadoId
        cursor.execute('SELECT f_finFermentacion_1,f_finFermentacion_2,f_finMaduracion FROM t_produccionestados WHERE t_produccionestados.id = %s' %(produccionEstadoId))
        datosConsulta=cursor.fetchone()
        self.finFase = datosConsulta
        #query = 'UPDATE SET f_produccionfasesid = 19 WHERE db.t_produccionestados.id = CambiarFase.estadoId'

        cursor.execute('SELECT t_fermentadores.f_nombrefermentador,t_perfilestemperatura.f_tempfermentacion_1,t_perfilestemperatura.f_tempfermentacion_2,t_perfilestemperatura.f_tempmaduracion,t_produccionestados.f_finFermentacion_1,t_produccionestados.f_finFermentacion_2,t_produccionestados.f_finMaduracion FROM t_produccionestados INNER JOIN t_fermentadores ON t_produccionestados.f_fermentador = t_fermentadores.id INNER JOIN t_perfilestemperatura ON t_produccionestados.f_perfilestemperaturaid = t_perfilestemperatura.id WHERE t_produccionestados.id=%s' %(produccionEstadoId))
        datosConsulta=cursor.fetchone()
        self.consulta = datosConsulta

        CambiarFase.fermentador = self.consulta['f_nombrefermentador']
        CambiarFase.temperaturas = self.consulta['f_tempfermentacion_1'],self.consulta['f_tempfermentacion_2'],self.consulta['f_tempmaduracion']
        CambiarFase.finFase = self.finFase


    def fermentacion_1(self):
        ASUNTO = "Alerta de cambio de fase en fermentador %s" %(str(CambiarFase.fermentador))
        if (CambiarFase.ahora > CambiarFase.finFase['f_finFermentacion_1']):
            if (CambiarFase.finFase['f_finFermentacion_2'] is None):
                query = 'UPDATE t_produccionestados SET f_produccionfasesid = 19 WHERE t_produccionestados.id = %s' %(CambiarFase.estadoId)

                cursor.execute(query)
                db.commit()
                serial_w('s',str(CambiarFase.fermentador),str(CambiarFase.temperaturas[2]))
                #print ("Se realiza cambio a fase maduracion en estadoid %s"%(estadoid))
                CUERPO = "Se realizo cambio de fase a maduracion en fermentador %s con temperatura %sºC" %(str(CambiarFase.fermentador),\
                    str(CambiarFase.temperaturas[2]))

                return 2
            else:
                query = 'UPDATE t_produccionestados SET f_produccionfasesid = 18 WHERE t_produccionestados.id = %s' %(CambiarFase.estadoId)

                cursor.execute(query)
                db.commit()
                serial_w('s',str(CambiarFase.fermentador),str(CambiarFase.temperaturas[1]))
                #print ("Se realiza cambio a fase fermentacion_2 en estadoid %s"%(estadoid))
                CUERPO = "Se realizo cambio de fase a fermentacion secundaria en fermentador %s con temperatura %sºC" %(str(CambiarFase.fermentador),\
                    str(CambiarFase.temperaturas[1]))
            
            EnviarCorreo(ASUNTO,CUERPO)
            
            return 1
        else:
            serial_w('s',str(CambiarFase.fermentador),str(CambiarFase.temperaturas[0]))
            #print ("Esta en fermentacion_1 y se mantiene fase en estadoid %s"%(estadoid))
            return 0

    def fermentacion_2(self):
        ASUNTO = "Alerta de cambio de fase en fermentador %s" %(str(CambiarFase.fermentador))
        if (CambiarFase.ahora > CambiarFase.finFase['f_finFermentacion_2']):
            query = 'UPDATE t_produccionestados SET f_produccionfasesid = 19 WHERE t_produccionestados.id = %s' %(CambiarFase.estadoId)

            cursor.execute(query)
            db.commit()
            serial_w('s',str(CambiarFase.fermentador),str(CambiarFase.temperaturas[2]))
            CUERPO = "Se realizo cambio de fase a maduracion en fermentador %s con temperatura %sºC" %(str(CambiarFase.fermentador),\
                str(CambiarFase.temperaturas[2]))

            EnviarCorreo(ASUNTO,CUERPO)
           
            return 1
        else:
            return 0

    def maduracion(self):
        ASUNTO = "Alerta de cambio de fase en fermentador %s" %(str(CambiarFase.fermentador))
        if (CambiarFase.ahora > CambiarFase.finFase['f_finMaduracion']):
            query = 'UPDATE t_produccionestados SET f_produccionfasesid = 20 WHERE t_produccionestados.id = %s' %(CambiarFase.estadoId)

            cursor.execute(query)
            db.commit()
            serial_w('s',str(CambiarFase.fermentador),str(CambiarFase.temperaturas[2]))
            CUERPO = "Fase de maduracion finalizada en fermentador %s con temperatura %sºC" %(str(CambiarFase.fermentador),str(CambiarFase.temperaturas[2]))

            EnviarCorreo(ASUNTO,CUERPO)

            return 1
        else:
            serial_w('s',str(CambiarFase.fermentador),str(CambiarFase.temperaturas[2]))
            return 0
# CONSULTAS
'''self.finFase = SELECT f_finFermentacion_1,f_finFermentacion_2,f_finMaduracion FROM t_produccionestados WHERE t_produccionestados.id = 14'

self.consulta = SELECT t_fermentadores.f_nombrefermentador,t_perfilestemperatura.f_tempfermentacion_1,t_perfilestemperatura.f_tempfermentacion_2,
t_perfilestemperatura.f_tempmaduracion,t_produccionestados.f_finFermentacion_1,t_produccionestados.f_finFermentacion_2,
t_produccionestados.f_finMaduracion FROM t_produccionestados
INNER JOIN t_fermentadores ON t_produccionestados.f_fermentador = t_fermentadores.id
INNER JOIN t_perfilestemperatura ON t_produccionestados.f_perfilestemperaturaid = t_perfilestemperatura.id
WHERE t_produccionestados.id=14
'''

# FUNCION PARA MONITOREO
def MonitorEstados(produccionEstadoId):
    estadoid = produccionEstadoId
    faseEstado = ComprobarFase(produccionEstadoId)
    faseCambio = CambiarFase(produccionEstadoId)
    faseActual = faseEstado.faseActual()

    print ("Fase actual: " + str(faseActual))

    if (faseActual == 2):
        fermentacion1 = faseCambio.fermentacion_1()

        print ("Cambio de fase?: " + str(fermentacion1))

        if (fermentacion1 == 0):
            print("Esta en fermentacion_1 y se mantiene fase en estadoid %s"%(estadoid))
        elif (fermentacion1 == 1):
            print ("Se realiza cambio a fase fermentacion_2 en estadoid %s"%(estadoid))
        elif (fermentacion1 == 2):
            print ("Se realiza cambio a fase maduracion en estadoid %s"%(estadoid))
        else:
            print ("No es posible determinar el fin de la fermentacion 1 en estadoid %s"%(estadoid))

    elif (faseActual == 3):
        fermentacion2 = faseCambio.fermentacion_2()
        print ("Cambio de fase?: " + str(fermentacion2))

        if (fermentacion2 == 0):
            print ("Esta en fermentacion_2 y se mantiene fase en estadoid %s"%(estadoid))
        elif (fermentacion2 == 1):
            print ("Se realiza cambio a fase maduracion en estadoid %s"%(estadoid))
        else:
            print ("No es posible determinar el fin de la fermentacion 2 en estadoid %s"%(estadoid))

    elif (faseActual == 4):
        maduracion = faseCambio.maduracion()
        print ("Cambio de fase?: " + str(maduracion))

        if (maduracion == 0):
            print ("Esta en maduracion y se mantiene fase en estadoid %s"%(estadoid))
        elif (maduracion == 1):
            print ("Fin de maduracion")
        else:
            print ("No es posible determinar el fin de la maduracion en estadoid %s"%(estadoid))

    elif (faseActual == 5):
        print ("Proceso finalizado, se mantiene la temperatura de proceso finalizado en estadoid %s"%(estadoid))

# FUNCION DE PRUEBAS
def BuscarActivos():
    query ="SELECT t_produccionestados.id FROM t_produccionestados WHERE f_activa = 'T'"
    consulta = MysqlQuery(query)
    activas = consulta.runQueryAsBasic()
    for row in activas:
        MonitorEstados(row)
        EstadoTemperaturas(row)


BuscarActivos()
