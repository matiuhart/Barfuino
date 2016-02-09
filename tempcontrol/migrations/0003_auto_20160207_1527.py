# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-07 18:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tempcontrol', '0002_remove_fermentadores_sensorid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ControlProcesos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coccion_num', models.IntegerField(verbose_name='Numero de cocción')),
                ('fechaInicio', models.DateField(blank=True, null=True)),
                ('fermentador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tempcontrol.Fermentadores')),
            ],
        ),
        migrations.CreateModel(
            name='TemperaturasHistorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperatura', models.DecimalField(decimal_places=2, max_digits=4)),
                ('fechaSensado', models.DateField(blank=True, null=True)),
                ('fermentador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tempcontrol.Fermentadores')),
            ],
        ),
        migrations.CreateModel(
            name='TemperaturasPerfiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('fermentacion1Fin', models.DateTimeField(blank=True, null=True)),
                ('fermentacion2Fin', models.DateTimeField(blank=True, null=True)),
                ('maduracionFin', models.DateField(verbose_name='Fin Maduracion')),
                ('clarificadoFin', models.DateField(verbose_name='Fin clarificado')),
                ('temperaturas', models.CharField(max_length=6)),
                ('descripcion', models.CharField(max_length=150)),
            ],
        ),
        migrations.RemoveField(
            model_name='temperaturas_historial',
            name='fermentador',
        ),
        migrations.RemoveField(
            model_name='temperaturas_historial',
            name='sensorId',
        ),
        migrations.AddField(
            model_name='sensores',
            name='mac',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.DeleteModel(
            name='Temperaturas_historial',
        ),
        migrations.AddField(
            model_name='temperaturashistorial',
            name='sensorId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tempcontrol.Sensores'),
        ),
        migrations.AddField(
            model_name='controlprocesos',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tempcontrol.Sensores'),
        ),
        migrations.AddField(
            model_name='controlprocesos',
            name='temperaturaPerfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tempcontrol.TemperaturasPerfiles'),
        ),
    ]