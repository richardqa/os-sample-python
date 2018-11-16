# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-31 11:52
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciudadano', '0007_auto_20170131_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciudadano',
            name='tipo_seguro',
            field=models.CharField(blank=True, choices=[('0', 'NO SE CONOCE'), ('1', 'USUARIO'), ('2', 'SIS'), ('3', 'ESSALUD'), ('4', 'S.O.A.T'), ('5', 'SANIDAD F.A.P'), ('6', 'SANIDAD NAVAL'), ('7', 'SANIDAD EP'), ('8', 'SANIDAD PNP'), ('9', 'PRIVADOS'), ('10', 'OTROS'), ('11', 'EXONERADO')], max_length=2, null=True, verbose_name='Tipo de seguro'),
        ),
        migrations.AlterField(
            model_name='ciudadanorn',
            name='financiador_parto',
            field=models.CharField(blank=True, choices=[('0', 'NO SE CONOCE'), ('1', 'USUARIO'), ('2', 'SIS'), ('3', 'ESSALUD'), ('4', 'S.O.A.T'), ('5', 'SANIDAD F.A.P'), ('6', 'SANIDAD NAVAL'), ('7', 'SANIDAD EP'), ('8', 'SANIDAD PNP'), ('9', 'PRIVADOS'), ('10', 'OTROS'), ('11', 'EXONERADO')], max_length=2, null=True, validators=[django.core.validators.RegexValidator(message='Numero de 2 digitos', regex='^[0-9]{2}$')], verbose_name='Financiador Parto'),
        ),
    ]