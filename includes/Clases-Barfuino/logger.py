#!/usr/bin/python
# -*- encoding: utf-8 -*-

import MySQLdb
import os
import time
import serial
from time import sleep
from datetime import datetime, timedelta
import glob


# BUSQUEDA DE PUERTOS AARDUINO
def serial_ports():
    ports = glob.glob('/dev/ttyACM[0-10]*')
    result = ""
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result=port
        except (OSError, serial.SerialException):
            pass
    return result


# LECTURA DE PUERTO SERIE
def serial_w(mode,ferm,temp=''):
	port=serial_ports()
	serie = serial.Serial(port,9600,timeout = 3)
	temperatura=''

	if (mode == 's'):
		serie.write(mode+ferm+temp)
		print mode+ferm+temp
	elif (mode == 'g'):
		serie.write(mode+ferm)
		time.sleep(1)
		while serie.inWaiting() > 0:
			temperatura += serie.read(1)
		return temperatura
		temperatura=''
	serie.close()


now = datetime.now()
fecha=now.strftime('%Y-%m-%d %H:%M:%S')

# VARIABLES PARA CONEXION DE DB
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = '114529'
DB_NAME = 'barfuino'

# FUNCION PARA CONEXION A DB
def run_query(query=''):
    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME]
    conn = MySQLdb.connect(*datos)
    cursor = conn.cursor()
    cursor.execute(query)

    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()

    else:
        conn.commit()
        data = None

    cursor.close()
    conn.close()

    return data

# FUNCION PARA BUSQUEDA DE FERMENTADORES ACTIVOS
def fermentadores_activos():
    query = "SELECT f_nombrefermentador FROM t_produccionestados JOIN t_fermentadores on t_produccionestados.f_fermentador = t_fermentadores.id WHERE t_produccionestados.f_activa = 'T'"
    fermentadores = run_query(query)
    for activo in fermentadores:
        fermentador = activo
        temp_hist(fermentador)

# FUNCION PARA CONSULTA E INSERSION DE TEMPERATURAS
def temp_hist(numFermentador):
	now = datetime.now()
	fecha=now.strftime('%Y-%m-%d %H:%M:%S')
	fermentadores = numFermentador
	for fermentador in fermentadores:
		fermentadorId = run_query("SELECT id FROM t_fermentadores WHERE f_nombrefermentador = %s" %(fermentador))
		serieout=serial_w('g',fermentador)
		time.sleep(2.5)
		#print serieout
		temp= int(serieout)
		print temp
		#print fermentadorId[0][0]
		if (temp > 0 and temp < 35 and temp != ""):
			query = "INSERT INTO t_temperaturashistorial (f_fechatemperatura,f_temperatura,f_fermentadoresid) VALUES ('%s','%s','%s')" % (fecha,temp,fermentadorId[0][0])
			run_query(query)
		else:
			temp_hist(fermentador)


fermentadores_activos()
#print("Temperatura " + str(temperatura))

# CODIGO PARA PRUEBAS
'''
try:
	while 1:
		fermentadores_activos()
		time.sleep(120)
except KeyboardInterrupt:
	        print "\ndone"


try:
	while 1:
		temperatura1 = serial_w('g','1')
		temperatura2 = serial_w('g','2')
		print("Sensor 1: " + str(temperatura1) + "\n")
		print("Sensor 2: " + str(temperatura2) + "\n")
		time.sleep(10)
except KeyboardInterrupt:
	print "\ndone"

'''

