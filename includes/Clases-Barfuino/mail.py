#!/usr/bin/python
# -*- encoding: utf-8 -*-

import serial
import time
import smtplib

USUARIO_MAIL = 'infraestructura@caminosprotegidos.com.ar'
CONTRASENA_MAIL = 'Protegidos2014*'

DESTINATARIO = 'matias_uhart@hotmail.com'
REMITENTE = 'infraestructura@caminosprotegidos.com.ar'

ASUNTO  = ' ¡ La temperatura exede los 26° ! '
MENSAJE = ' ¡ Su sensor de temperatura ha detectado que la misma es superior al los 26° ! '

arduino = serial.Serial('/dev/ttyACM1', 9600, timeout = 3.0)    #El puerto se abre inmediatamente en la creación de objetos, cuando se da un puerto.


mailSend = 0

def enviar_correo_electronico():
    print("Envíando e-mail")
    smtpserver = smtplib.SMTP("smtp.caminosprotegidos.com.ar",25)     #Definimos el objeto 'smtpserver' con smptlib.SMTP, SMTP("",) Administra la conexión SMTP
    smtpserver.ehlo()                                   #Este método prepara envíar un correo electrónico
    smtpserver.starttls()                               #Pone la conexión con el servidor SMTP en el modo de TLS.
    smtpserver.ehlo()
    smtpserver.login(USUARIO_MAIL, CONTRASENA_MAIL)   #Iniciamos sesion en el SMTP server de Google
    header  = 'To:      ' + DESTINATARIO + '\n'         #Construimos el 'HEADER' para envíar el correo electrónico       
    header += 'From:    ' + REMITENTE    + '\n'
    header += 'Subject: ' + ASUNTO       + '\n'
    print header
    msg = header + '\n' + MENSAJE + ' \n\n'             #Concatenamos el'HEADER' y el 'MENSAJE' del correo electrónico
    smtpserver.sendmail(REMITENTE, DESTINATARIO, msg)   #Envíamos el correo electrónico
    smtpserver.close()                                  #Cerramos la conexión con el SMTP server de Google

while True:
	lineaLeida = arduino.readline()
	print lineaLeida
	if int(lineaLeida) >= 32 :
		print "La temperatura es alta"
		enviar_correo_electronico()
        	mailSend+=1
        	if mailSend >= 1 :
			time.sleep(10)
		else :
			print lineaLeida

#while True:
#    lineaLeida = arduino.readline()                     #Guardo una línea leída desde el puerto serial
#    print lineaLeida
#    if int(lineaLeida) >= 34 :                           #Si la línea contiene a 'H' envía un correo electrónico
#        enviar_correo_electronico()                     #Envío un correo electrónico 
#    time.sleep(0.5)


# EOF
