#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
Estas funciones realizan el monitoreo de las temperaturas en los fermentadores. Verifica en la base de datos si el tiempo del ultimo 
sensado de temperatura es menor a 45 minutos o si la temperatura se mantuvo por arriba de la correspondiente por mas del tiempo mencionado anterioirmente, 
de ser mayor en cualquiera de los dos casos, envia una alerta via email con el aviso de problemas de sensado
'''
from dbconn import *
from notificaciones import *
from datetime import time
import datetime

# Resta de minutos de medicion anterior
def RestarMinutos(minutos=0):
    hora = datetime.datetime.now() - datetime.timedelta(minutes=minutos)
    nuevaHora = hora.strftime("%Y-%m-%d %H:%M:%S")
    return nuevaHora

# def EstadoArduino(produccionEstadoId):

def EstadoTemperaturas(produccionEstadoId):
    query = "SELECT t_fermentadores.f_nombrefermentador,t_produccionfases.f_nombre,t_perfilestemperatura.f_tempfermentacion_1, \
    t_perfilestemperatura.f_tempfermentacion_2,t_perfilestemperatura.f_tempmaduracion FROM t_produccionestados \
    INNER JOIN t_fermentadores ON t_produccionestados.f_fermentador = t_fermentadores.id \
    INNER JOIN t_perfilestemperatura ON t_produccionestados.f_perfilestemperaturaid = t_perfilestemperatura.id \
    INNER JOIN t_produccionfases ON t_produccionestados.f_produccionfasesid = t_produccionfases.id \
    WHERE t_produccionestados.id=%s" %(produccionEstadoId)

    # Recupero todos los nombre de fermentador, fase y temperaturas seteadas desde la BD para el fermentador con produccionEstadoId x
    conexion = MysqlQuery(query)
    resultado = conexion.runQueryAsDictAll()
    datos = resultado[0]

    fermentador = datos['f_nombrefermentador']
    fase = datos['f_nombre']
    temperaturasPerfil = datos['f_tempfermentacion_1'],datos['f_tempfermentacion_2'], datos['f_tempmaduracion']


    # Recupero temperatura para fase actual de fermentador
    temperaturaFase = 0
    if (fase == 2):
        temperaturaFase = int(temperaturasPerfil[0])
    elif (fase == 3):
        temperaturaFase = int(temperaturasPerfil[1])
    elif (fase == 4):
        temperaturaFase = int(temperaturasPerfil[2])


    # Cantidad de minutos pasados de ultima medicion de temperatura para enviar alerta
    hora = RestarMinutos(45)
    temperaturasHistorial = "SELECT f_temperatura FROM t_temperaturashistorial WHERE f_fermentadoresid='%s' AND f_fechatemperatura > '%s';" %(fermentador,hora)

    conexion = MysqlQuery(temperaturasHistorial)
    resultadoTemps = conexion.runQueryAsDictAll()

    if (resultado):
        temperaturas = int(resultadoTemps[0]['f_temperatura']),int(resultadoTemps[1]['f_temperatura']),int(resultadoTemps[2]['f_temperatura'])
	print "El valor de datos es " +str(datos)

        if ((temperaturas[0] > temperaturaFase) & (temperaturas[1] > temperaturaFase) & (temperaturas[2] > temperaturaFase)):
            CUERPO = 'En los ultimos 45 min las temperaturas exeden los %s° C seteados, las ultimas mediciones son %s° C'%(temperaturaFase,temperaturas)
            ASUNTO = 'Temperaturas Altas en Fermentador %s'%(fermentador)

            EnviarCorreo(ASUNTO,CUERPO)

            #print "\n ENVIAR NOTIFICACION DE TEMPERATURAS ALTAS \n"
            #print("\n LAS ULTIMAS TEMPERATURAS SON" + str(datos[0]) + str(datos[1]) + str(datos[2]) + "\n")

        else:
            print "\n NO HAY ALERTAS \n"
            print("\n LAS ULTIMAS TEMPERATURAS SON" + str(resultadoTemps[0]) + str(resultadoTemps[1]) + str(resultadoTemps[2]) + "\n")

    else:
        CUERPO = 'En los ultimos 45 min las temperaturas no pudieron ser sensadas en el fermentador %s, por favor verifique el sistema'%(fementador)
        ASUNTO = 'Problema de Sensado de Temperaturas en Fermentador %s'%(fermentador)

        EnviarCorreo(ASUNTO,CUERPO)

        print "\n ENVIAR ALERTA DE PROBLEMA AL SENSAR TEMPERATURA \n"



    print("\n FASE ACTUAL: " + str(fase))

    print("\n LA TEMEPERATURA DE FASE ES: " + str(temperaturaFase) + "\n")































