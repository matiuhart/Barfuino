# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-14 02:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tempcontrol', '0026_configuraciones'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperaturasperfiles',
            name='temperaturas',
            field=models.CommaSeparatedIntegerField(max_length=14),
        ),
    ]
