# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0003_auto_20170303_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipopersonal',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
    ]