# Generated by Django 3.1.1 on 2021-03-29 01:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0009_auto_20201214_1442'),
        ('attendancess', '0008_attendanceidmodel_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendanceidmodel',
            name='classroom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='classroom.classroommodel'),
        ),
    ]
