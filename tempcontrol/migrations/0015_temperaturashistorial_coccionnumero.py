# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-07 22:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tempcontrol', '0014_auto_20160207_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='temperaturashistorial',
            name='coccionNumero',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='tempcontrol.ControlProcesos'),
        ),
    ]
