# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-10 18:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tempcontrol', '0018_auto_20160210_0151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlprocesos',
            name='fermentador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fermentadorId', to='tempcontrol.Fermentadores'),
        ),
    ]