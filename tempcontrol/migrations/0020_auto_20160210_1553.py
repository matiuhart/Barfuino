# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-10 18:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tempcontrol', '0019_auto_20160210_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlprocesos',
            name='clarificadoFin',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Clarificado'),
        ),
        migrations.AlterField(
            model_name='controlprocesos',
            name='fechaInicio',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Inicio de proceso'),
        ),
        migrations.AlterField(
            model_name='controlprocesos',
            name='fermentado1Fin',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fermentado 1'),
        ),
        migrations.AlterField(
            model_name='controlprocesos',
            name='fermentado2Fin',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fermentado 2'),
        ),
        migrations.AlterField(
            model_name='controlprocesos',
            name='fermentador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tempcontrol.Fermentadores'),
        ),
        migrations.AlterField(
            model_name='controlprocesos',
            name='maduradoFin',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Madurado'),
        ),
        migrations.AlterField(
            model_name='temperaturashistorial',
            name='fechaSensado',
            field=models.DateTimeField(blank=True, null=True, verbose_name='fecha de sensado'),
        ),
    ]
