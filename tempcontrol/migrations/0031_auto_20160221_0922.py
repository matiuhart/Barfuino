# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-21 12:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tempcontrol', '0030_auto_20160221_0919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temperaturashistorial',
            old_name='coccionNum',
            new_name='coccionNumero',
        ),
    ]
