# Generated by Django 3.1.1 on 2021-03-25 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendancess', '0004_remove_attendanceidmodel_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendanceidmodel',
            name='hour',
            field=models.PositiveIntegerField(choices=[(1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'), (5, 'V')], default=1),
            preserve_default=False,
        ),
    ]