# Generated by Django 2.0.1 on 2018-01-24 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20171002_0833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='about_me',
        ),
    ]
