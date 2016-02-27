#!/usr/bin/python3.4
# -*- encoding: utf-8 -*-

import os
import sys
import django

def djangoPath():
	sys.path.append("/home/barfuino")
	os.environ["DJANGO_SETTINGS_MODULE"] = "barfuino.settings"
	django.setup()
djangoPath()
from tempcontrol.models import *


