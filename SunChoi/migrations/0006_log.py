# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 11:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('SunChoi', '0005_auto_20170823_0411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id_log', models.AutoField(primary_key=True, serialize=False)),
                ('razon_social', models.CharField(max_length=200)),
                ('id_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]