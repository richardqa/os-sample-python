# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-04 15:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('ciudadano', '0034_auto_20170425_1249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='antecedenteciudadano',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='antecedentefamiliar',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='ciudadano',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='ciudadanorn',
            name='uuid',
        ),
    ]
