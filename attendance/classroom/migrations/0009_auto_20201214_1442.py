# Generated by Django 3.1.1 on 2020-12-14 09:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classroom', '0008_classroommodel_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroommodel',
            name='students',
            field=models.ManyToManyField(limit_choices_to={'user_type': 3}, related_name='classroom_students', to=settings.AUTH_USER_MODEL),
        ),
    ]
