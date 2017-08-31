# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0009_entry_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='learning_logs.Topic'),
        ),
    ]