# Generated by Django 3.1.1 on 2021-05-16 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0013_auto_20210502_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hourmodel',
            name='semester',
            field=models.PositiveBigIntegerField(choices=[(1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'), (5, 'V'), (6, 'VI')]),
        ),
    ]
