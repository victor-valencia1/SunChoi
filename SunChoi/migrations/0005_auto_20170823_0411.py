# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 04:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('SunChoi', '0004_auto_20170823_0409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordencompra',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]