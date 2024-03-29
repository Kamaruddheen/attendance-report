# Generated by Django 3.2 on 2023-12-09 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attendancess', '0002_attendanceidmodel_classroom'),
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendanceidmodel',
            name='hour_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subject.hourmodel'),
        ),
        migrations.AddField(
            model_name='attendanceidmodel',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subject.subjectmodel'),
        ),
    ]
