# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0013_auto_20170918_0710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]