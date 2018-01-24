# Generated by Django 2.0.1 on 2018-01-24 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0020_auto_20170929_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(choices=[('primary', 'Blue'), ('secondary', 'Gray'), ('success', 'Green'), ('info', 'Cyan'), ('warning', 'Yellow'), ('danger', 'Red'), ('light', 'White'), ('dark', 'Black')], default='primary', max_length=10),
        ),
    ]
