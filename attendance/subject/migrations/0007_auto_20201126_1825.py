# Generated by Django 3.1.1 on 2020-11-26 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0006_auto_20201125_0935'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subjectmodel',
            options={'verbose_name': 'Subject', 'verbose_name_plural': 'Subjects'},
        ),
        migrations.AlterModelTable(
            name='subjectmodel',
            table='subject',
        ),
    ]
