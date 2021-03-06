# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ciudadano', '0025_auto_20170306_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='CiudadanoParentesco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titular', models.CharField(max_length=12, verbose_name='Nro Documento Persona')),
                ('pariente', models.CharField(max_length=12, verbose_name='Nro Documento Pariente')),
                ('parentesco', models.PositiveSmallIntegerField(choices=[(1, 'Padre'), (2, 'Madre'), (3, 'Hijo(a)')])),
            ],
        ),
    ]
