# Generated by Django 3.2 on 2023-12-09 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HourModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('hour_type', models.CharField(choices=[('core', 'Core'), ('noncore', 'Non-Core'), ('sel', 'Selective'), ('lab', 'Lab')], max_length=10)),
            ],
            options={
                'verbose_name': 'Hour',
                'verbose_name_plural': 'Hours',
                'db_table': 'hour',
            },
        ),
        migrations.CreateModel(
            name='SubjectModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(max_length=50)),
                ('sub_count', models.PositiveBigIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
                'db_table': 'subject',
            },
        ),
    ]