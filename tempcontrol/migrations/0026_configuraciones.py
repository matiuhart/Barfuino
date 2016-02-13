# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-13 21:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tempcontrol', '0025_temperaturashistorial_activo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuraciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperaturaClarificado', models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name='Temperatura de Clarificado por Defecto')),
                ('temperaturaFinalizado', models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name='Temperatura de Finalizado por Defecto')),
                ('brewerMail', models.EmailField(max_length=100, null=True)),
            ],
        ),
    ]
