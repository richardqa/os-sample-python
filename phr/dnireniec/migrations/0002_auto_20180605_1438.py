# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-05 14:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dnireniec', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ServicioReniec',
        ),
        migrations.DeleteModel(
            name='ServicioSis',
        ),
    ]