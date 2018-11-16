# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 14:28
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ciudadano', '0040_auto_20170606_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciudadanorn',
            name='atiende_parto',
            field=models.CharField(blank=True, choices=[('00', 'NO SE CONOCE'), ('01', 'MEDICO'), ('02', 'OBSTETRA'),
                                                        ('03', 'ENFERMERA (O)'), ('04', 'INTERNA (O)'),
                                                        ('05', 'TECNICO SALUD'), ('06', 'PROMOTOR SALUD'),
                                                        ('07', 'PARTERA / COMADRONA'), ('08', 'FAMILIAR'),
                                                        ('09', 'OTRO'), ('10', 'NADIE (AUTOAYUDA)'),
                                                        ('11', 'MEDICO GINECO-OBSTETRA'), ('16', 'MEDICO RESIDENTE'),
                                                        ('99', 'NO REGISTRADO')], max_length=2, null=True, validators=[
                django.core.validators.RegexValidator(message='Numero de 2 digitos', regex='^[0-9]{2}$')],
                                   verbose_name='Responsable Atención'),
        ),
    ]
