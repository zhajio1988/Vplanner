# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 08:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0015_auto_20171028_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationlogs',
            name='name',
            field=models.CharField(default='None', editable=False, max_length=128, verbose_name='change by whom'),
        ),
    ]