# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-14 01:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SunChoi', '0006_auto_20170814_0137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='fecha_vencimiento',
        ),
    ]