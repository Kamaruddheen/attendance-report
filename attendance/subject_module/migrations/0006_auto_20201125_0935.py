# Generated by Django 3.1.1 on 2020-11-25 04:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timetable', '0001_initial'),
        ('classroom', '0005_auto_20201120_1922'),
        ('subject_module', '0005_auto_20201120_1922'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subject',
            new_name='SubjectModel',
        ),
    ]
