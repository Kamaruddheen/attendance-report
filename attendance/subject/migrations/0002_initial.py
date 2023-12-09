# Generated by Django 3.2 on 2023-12-09 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subject', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classroom', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectmodel',
            name='handled_by',
            field=models.ForeignKey(limit_choices_to=models.Q(user_type=2), on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subjectmodel',
            name='hour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='subject.hourmodel'),
        ),
        migrations.AddField(
            model_name='subjectmodel',
            name='students',
            field=models.ManyToManyField(blank=True, limit_choices_to={'user_type': 3}, related_name='students', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hourmodel',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.classroommodel'),
        ),
    ]