# Generated by Django 3.1.1 on 2021-01-07 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0007_auto_20201126_1825'),
        ('timetable', '0015_auto_20201214_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetablemodel',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subject.subjectmodel'),
        ),
    ]
