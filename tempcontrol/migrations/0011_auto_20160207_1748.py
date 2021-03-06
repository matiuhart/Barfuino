# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-07 20:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tempcontrol', '0010_controlprocesos_activo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensores',
            name='fermentadorId',
        ),
        migrations.AddField(
            model_name='sensores',
            name='fermentador',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='tempcontrol.Fermentadores'),
        ),
        migrations.AlterField(
            model_name='controlprocesos',
            name='fechaInicio',
            field=models.DateField(blank=True, null=True, verbose_name='fecha de inicio de proceso'),
        ),
        migrations.AlterField(
            model_name='controlprocesos',
            name='temperaturaPerfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tempcontrol.TemperaturasPerfiles', verbose_name='Perfil de Temperatura'),
        ),
        migrations.AlterField(
            model_name='temperaturashistorial',
            name='fechaSensado',
            field=models.DateField(blank=True, null=True, verbose_name='fecha de sensado'),
        ),
        migrations.AlterField(
            model_name='temperaturasperfiles',
            name='clarificadoFin',
            field=models.DateField(blank=True, verbose_name='Final Clarificación'),
        ),
        migrations.AlterField(
            model_name='temperaturasperfiles',
            name='descripcion',
            field=models.CharField(max_length=200, verbose_name='descripción'),
        ),
        migrations.AlterField(
            model_name='temperaturasperfiles',
            name='fermentacion1Fin',
            field=models.DateField(blank=True, null=True, verbose_name='Final 1er Fermentación'),
        ),
        migrations.AlterField(
            model_name='temperaturasperfiles',
            name='fermentacion2Fin',
            field=models.DateField(blank=True, null=True, verbose_name='Final 2da Fermentación'),
        ),
        migrations.AlterField(
            model_name='temperaturasperfiles',
            name='maduracionFin',
            field=models.DateField(blank=True, verbose_name='Final Maduración'),
        ),
    ]
