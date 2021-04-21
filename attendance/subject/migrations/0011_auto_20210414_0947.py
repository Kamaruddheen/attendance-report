# Generated by Django 3.1.1 on 2021-04-14 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0010_auto_20210325_0704'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectmodel',
            name='sub_count',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='hourmodel',
            name='hour_type',
            field=models.CharField(choices=[('core', 'Core'), ('noncore', 'Non-Core'), ('sel', 'Selective'), ('lab', 'Lab')], max_length=10),
        ),
        migrations.AlterModelTable(
            name='hourmodel',
            table='hour',
        ),
    ]