# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-25 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciudadano', '0062_domiciliociudadanohistorial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciudadano',
            name='origen_datos',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'importado'), (2, 'hisminsa'), (3, 'búsqueda reniec'), (4, 'cnv'), (5, 'creado'), (6, 'búsqueda migraciones')], default=5, null=True),
        ),
    ]