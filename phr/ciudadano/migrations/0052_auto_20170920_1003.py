# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 10:03
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


def actualiza_ciex_antecedentes(apps, schema_editor):
    AntecedenteModel = apps.get_model('ciudadano', 'AntecedenteCiudadano')
    CiexModel = apps.get_model('catalogo', 'CatalogoCIE')
    antecedentes = AntecedenteModel.objects.all().iterator()
    for obj in antecedentes:
        try:
            ciex = CiexModel.objects.get(id=obj.ciex)
            obj.ciex = ciex.id_ciex
            obj.save()
        except Exception as ex:
            pass


def actualiza_ciex_antecedentes_rev(apps, schema_editor):
    AntecedenteModel = apps.get_model('ciudadano', 'AntecedenteCiudadano')
    CiexModel = apps.get_model('catalogo', 'CatalogoCIE')
    antecedentes = AntecedenteModel.objects.all().iterator()
    for obj in antecedentes:
        try:
            ciex = CiexModel.objects.get(id_ciex=obj.ciex)
            obj.ciex = ciex.id
            obj.save()
        except Exception as ex:
            pass


def actualiza_ciex_antecedentes_fam(apps, schema_editor):
    AntecedenteModel = apps.get_model('ciudadano', 'AntecedenteFamiliar')
    CiexModel = apps.get_model('catalogo', 'CatalogoCIE')
    antecedentes = AntecedenteModel.objects.all().iterator()
    for obj in antecedentes:
        try:
            ciex = CiexModel.objects.get(id=obj.ciex)
            obj.ciex = ciex.id_ciex
            obj.save()
        except Exception as ex:
            pass


def actualiza_ciex_antecedentes_fam_rev(apps, schema_editor):
    AntecedenteModel = apps.get_model('ciudadano', 'AntecedenteFamiliar')
    CiexModel = apps.get_model('catalogo', 'CatalogoCIE')
    antecedentes = AntecedenteModel.objects.all().iterator()
    for obj in antecedentes:
        try:
            ciex = CiexModel.objects.get(id_ciex=obj.ciex)
            obj.ciex = ciex.id
            obj.save()
        except Exception as ex:
            pass


class Migration(migrations.Migration):
    dependencies = [
        ('ciudadano', '0051_antecedentemedicacionhabitual'),
    ]

    operations = [
        migrations.AddField(
            model_name='antecedenteciudadano',
            name='codigo_antecedente_sugerido',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='antecedenteciudadano',
            name='nombre_antecedente_sugerido',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='antecedentefamiliar',
            name='codigo_antecedente_sugerido',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='antecedentefamiliar',
            name='nombre_antecedente_sugerido',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='antecedenteciudadano',
            name='ciex',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='antecedentefamiliar',
            name='ciex',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='antecedentefamiliar',
            name='fecha_fin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='antecedentefamiliar',
            name='fecha_inicio',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='antecedenteciudadano',
            name='tipo_antecedente',
            field=models.CharField(blank=True,
                                   choices=[('1', 'Personal'), ('2', 'Gineco-Obstetra'), ('3', 'Patológico'),
                                            ('4', 'Psicológico')], default='1', max_length=1, null=True),
        ),
        migrations.RemoveField(
            model_name='antecedentefamiliar',
            name='parentesco',
        ),
        migrations.AddField(
            model_name='antecedentefamiliar',
            name='parentesco',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveSmallIntegerField(
                    blank=True,
                    choices=[('1', 'Padre'), ('2', 'Madre'), ('3', 'Hermanos'), ('4', 'Otros')], null=True),
                null=True, size=None),
        ),
        migrations.RunPython(actualiza_ciex_antecedentes, actualiza_ciex_antecedentes_rev),
        migrations.RunPython(actualiza_ciex_antecedentes_fam, actualiza_ciex_antecedentes_fam_rev),
    ]
