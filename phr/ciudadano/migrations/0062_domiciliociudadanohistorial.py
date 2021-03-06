# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-11 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ubigeo', '0011_auto_20170508_1826'),
        ('ciudadano', '0061_auto_20180213_1146'),
    ]

    operations = [
        migrations.CreateModel(
            name='DomicilioCiudadanoHistorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domicilio_direccion', models.CharField(blank=True, max_length=500, null=True)),
                ('domicilio_referencia', models.CharField(blank=True, max_length=500, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('ciudadano', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ciudadano.Ciudadano')),
                ('departamento_domicilio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ubigeo.UbigeoDepartamento')),
                ('distrito_domicilio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ubigeo.UbigeoDistrito')),
                ('localidad_domicilio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ubigeo.UbigeoLocalidad')),
                ('pais_domicilio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ubigeo.UbigeoPais')),
                ('provincia_domicilio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ubigeo.UbigeoProvincia')),
            ],
        ),
    ]
