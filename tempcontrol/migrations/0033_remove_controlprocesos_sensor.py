# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-04 18:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tempcontrol', '0032_auto_20160227_2155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controlprocesos',
            name='sensor',
        ),
    ]
