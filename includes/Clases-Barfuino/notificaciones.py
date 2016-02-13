#!/usr/bin/python
# -*- encoding: utf-8 -*-

import serial
import time
import smtplib

USUARIO_MAIL = 'matias@mtu-it.com.ar'
CONTRASENA_MAIL = 'Martina84*29*12?'

DESTINATARIO = 'matias_uhart1@hotmail.com'
REMITENTE = 'barfuino@mtu-it.com.ar'


mailSend = 0

def EnviarCorreo(ASUNTO,MENSAJE):

    print("Envíando e-mail")
    smtpserver = smtplib.SMTP("smtp.gmail.com",25)     #Definimos el objeto 'smtpserver' con smptlib.SMTP, SMTP("",) Administra la conexión SMTP
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
    print "se cerro la conexion con el servidor"
