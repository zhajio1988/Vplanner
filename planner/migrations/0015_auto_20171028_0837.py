# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 08:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0014_auto_20171028_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationlogs',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='create date'),
        ),
        migrations.AlterField(
            model_name='operationlogs',
            name='mod_date',
            field=models.DateTimeField(auto_now=True, verbose_name='lastest modify date'),
        ),
    ]
