# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 17:21
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('establecimiento', '0005_establecimientosector'),
    ]

    operations = [
        migrations.AddField(
            model_name='establecimiento',
            name='sector',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE,
                                    to='establecimiento.EstablecimientoSector'),
        ),
        migrations.AlterField(
            model_name='establecimientosector',
            name='codigo',
            field=models.CharField(max_length=2, unique=True),
        ),
    ]
