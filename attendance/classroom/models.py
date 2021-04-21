from django.db import models
from django.conf import settings


class ClassroomModel(models.Model):
    course = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField(
        choices=((1, 'I'), (2, 'II'), (3, 'III')))
    sec = models.CharField(choices=(('a', 'A'), ('b', 'B')),
                           null=True, blank=True, max_length=5)
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to={'user_type': 2})
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='classroom_students', limit_choices_to={'user_type': 3})

    class Meta:
        db_table = 'classroom'
        verbose_name = 'Classroom'
        verbose_name_plural = 'Classrooms'

    def __str__(self):
        return self.get_year_display()+' '+self.course+' '+self.sec
