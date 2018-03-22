# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-29 05:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0022_remove_feature_self_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='views',
            new_name='likes',
        ),
        migrations.AddField(
            model_name='changelist',
            name='comment',
            field=models.CharField(default=1, max_length=128, verbose_name='change comments'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='featuredetail',
            name='func_cov_req',
            field=models.CharField(max_length=128, verbose_name='Func Cov Requirement'),
        ),
        migrations.AlterField(
            model_name='featuredetail',
            name='seq_req',
            field=models.CharField(max_length=128, verbose_name='Sequence Requirement'),
        ),
        migrations.AlterField(
            model_name='featuredetail',
            name='sim_req',
            field=models.CharField(max_length=128, verbose_name='Simulation Requirement'),
        ),
        migrations.AlterField(
            model_name='project',
            name='pid',
            field=models.IntegerField(default=0),
        ),
    ]
