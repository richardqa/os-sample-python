# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-11 14:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('ubigeo', '0007_ubigeocontinente_continente_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ubigeopais',
            old_name='id_pais',
            new_name='alpha3',
        ),
    ]