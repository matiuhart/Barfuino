#!/usr/bin/python3.4
# -*- encoding: utf-8 -*-

import os
import sys
import django
import platform

plataforma = platform.dist()
'''
def djangoPath():
	if plataforma[0] == 'debian':
		sys.path.append("/home/barfuino")
		os.environ["DJANGO_SETTINGS_MODULE"] = "barfuino.settings"
		django.setup()
	
	elif plataforma[0] == 'Linuxmint':
		sys.path.append("/home/mati/bin/django/barfuino")
		os.environ["DJANGO_SETTINGS_MODULE"] = "barfuino.settings"
		django.setup()
'''

def djangoPath():
	sys.path.append("/home/mati/bin/django/barfuino")
	os.environ["DJANGO_SETTINGS_MODULE"] = "barfuino.settings"
	django.setup()

djangoPath()
from tempcontrol.models import *

