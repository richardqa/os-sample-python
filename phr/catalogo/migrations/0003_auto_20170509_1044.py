# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-09 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0002_auto_20170421_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogoprocedimiento',
            name='codigo_cpt',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='catalogoprocedimiento',
            name='codigo_grupo',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='catalogoprocedimiento',
            name='denominacion_procedimientos',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='catalogoprocedimiento',
            name='nombre_grupo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
