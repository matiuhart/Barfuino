# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-15 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tempcontrol', '0028_fermentadores_arduinoid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlprocesos',
            name='fermentado2Fin',
            field=models.DateTimeField(blank=True, default='', null=True, verbose_name='Fermentado 2'),
        ),
    ]
