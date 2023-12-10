from django.db import models

from classroom.models import ClassroomModel
from subject.models import SubjectModel, HourModel


class TimetablesetModel(models.Model):
    name = models.CharField(max_length=50, blank=True)
    classroom = models.ForeignKey(ClassroomModel, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()

    class Meta:
        db_table = 'set'
        verbose_name = 'Set'
        verbose_name_plural = 'Sets'

    def __str__(self):
        # foriegn key data are not string ;they belong to the particular model so we have to convert that to string to concatenate with the string
        return self.name + " ( " + self.from_date.strftime("%d") + "-" + self.from_date.strftime("%b") + "-" + self.from_date.strftime("%Y") + " ) to ( " + self.to_date.strftime("%d") + "-" + self.to_date.strftime("%b") + "-" + self.to_date.strftime("%Y") + " )"


day_choices = (
    (1, 'I'),
    (2, 'II'),
    (3, 'III'),
    (4, 'IV'),
    (5, 'V'),
    (6, 'VI')
)

hour_choices = (
    (1, 'I'),
    (2, 'II'),
    (3, 'III'),
    (4, 'IV'),
    (5, 'V')
)


class TimetableModel(models.Model):
    hour = models.PositiveIntegerField(choices=hour_choices)
    day = models.PositiveIntegerField(choices=day_choices)
    subject = models.ForeignKey(
        HourModel, on_delete=models.CASCADE, null=True, blank=True)
    set_name = models.ForeignKey(TimetablesetModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'timetable'
        verbose_name = 'Timetable'
        verbose_name_plural = 'Timetables'

    def __str__(self):
        if self.subject is None:
            return "TBD"
        else:
            return self.subject.name
