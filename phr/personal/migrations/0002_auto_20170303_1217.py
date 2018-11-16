# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('establecimiento', '0002_auto_20170301_1027'),
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personal',
            old_name='inforrus',
            new_name='inforhus',
        ),
        migrations.AddField(
            model_name='personal',
            name='cmp',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='personal',
            name='establecimientos',
            field=models.ManyToManyField(to='establecimiento.Establecimiento'),
        ),
    ]