# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 09:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0018_auto_20171028_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationlogs',
            name='feature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planner.Feature'),
        ),
        migrations.AlterField(
            model_name='operationlogs',
            name='name',
            field=models.CharField(default=None, max_length=128, verbose_name='feature name'),
        ),
    ]