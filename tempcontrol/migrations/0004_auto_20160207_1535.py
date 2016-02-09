# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-07 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tempcontrol', '0003_auto_20160207_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fermentadores',
            name='nombre',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='temperaturasperfiles',
            name='clarificadoFin',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='temperaturasperfiles',
            name='descripcion',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='temperaturasperfiles',
            name='fermentacion1Fin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='temperaturasperfiles',
            name='fermentacion2Fin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='temperaturasperfiles',
            name='maduracionFin',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='temperaturasperfiles',
            name='temperaturas',
            field=models.CharField(max_length=10),
        ),
    ]
