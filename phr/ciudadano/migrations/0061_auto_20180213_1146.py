# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-13 11:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciudadano', '0060_auto_20180123_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antecedenteciudadano',
            name='subgrupo_antecedente',
            field=models.CharField(blank=True, choices=[('1', 'Patológicos'), ('2', 'Lesiones premalignas'), ('3', 'Cáncer'), ('4', 'Salud mental'), ('5', 'Intervenciones quirúrgicas')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='antecedentefamiliar',
            name='subgrupo_antecedente',
            field=models.CharField(blank=True, choices=[('1', 'Patológicos'), ('2', 'Lesiones premalignas'), ('3', 'Cáncer'), ('4', 'Salud mental'), ('5', 'Intervenciones quirúrgicas')], max_length=1, null=True),
        ),
    ]
