# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0011_entry_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='topic',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('default', 'Gray'), ('primary', 'Blue'), ('success', 'Green'), ('info', 'Cyan'), ('warning', 'Yellow'), ('danger', 'Red')], default='default', max_length=10)),
                ('title', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='tag',
            field=models.ManyToManyField(blank=True, default='', to='learning_logs.Tag'),
        ),
    ]
