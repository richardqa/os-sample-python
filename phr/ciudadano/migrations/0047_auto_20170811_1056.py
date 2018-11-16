# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-11 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciudadano', '0046_ciudadanodatossis'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciudadanodatossis',
            name='genero',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='ciudadanodatossis',
            name='id_ubigeo',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='ciudadanodatossis',
            name='tabla',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='ciudadanodatossis',
            name='tipo_documento',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]