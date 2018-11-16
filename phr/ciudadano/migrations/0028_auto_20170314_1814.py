# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-14 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ciudadano', '0027_auto_20170310_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciudadano',
            name='origen_datos',
            field=models.PositiveSmallIntegerField(blank=True,
                                                   choices=[(1, 'local'), (2, 'hisminsa'), (3, 'busqueda reniec'),
                                                            (4, 'cnv')], default=1, null=True),
        ),
    ]
