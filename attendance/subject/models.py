from django.conf import settings
from django.urls import reverse
from django.db import models

from classroom.models import ClassroomModel

sem_choice = (
    (1, 'I'),
    (2, 'II'),
    (3, 'III'),
    (4, 'IV'),
    (5, 'V'),
    (6, 'VI')
)


class HourModel(models.Model):
    name = models.CharField(max_length=50)  # Lang, EDC, SE, PCD...
    classroom = models.ForeignKey(ClassroomModel, on_delete=models.CASCADE)
    semester = models.PositiveBigIntegerField(choices=sem_choice)
    hour_type = models.CharField(max_length=10, choices=(
        ('core', 'Core'), ('noncore', 'Non-Core'), ('sel', 'Selective'), ('lab', 'Lab')))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subject:hour_detail', args=[self.classroom.id, self.id])

    def get_edit_url(self):
        return reverse('subject:edit_hour', args=[self.classroom.id, self.id])

    class Meta:
        db_table = 'hour'
        verbose_name = 'Hour'
        verbose_name_plural = 'Hours'


class SubjectModel(models.Model):
    # Software Engineering, Tamil, French
    sub_name = models.CharField(max_length=50)
    hour = models.ForeignKey(HourModel, on_delete=models.CASCADE, null=True)
    sub_code = models.CharField(max_length=15)
    handled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to=models.Q(user_type=2))  # Staff
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'user_type': 3},
        related_name="students",
        blank=True)  # null=True is not required for manytomany field, just blank will do
    sub_count = models.PositiveBigIntegerField(
        default=0)  # for timetable generation purpose

    def __str__(self):
        return self.sub_name

    def get_add_student_url(self):
        return reverse('subject:hour_add_students', args=[self.hour.classroom.id, self.hour.id, self.id])

    class Meta:
        db_table = 'subject'
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
