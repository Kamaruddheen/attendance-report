from django.conf import settings
from django.db import models
from subject.models import SubjectModel, HourModel

hour_choices = (
    (1, 'I'),
    (2, 'II'),
    (3, 'III'),
    (4, 'IV'),
    (5, 'V')
)


class AttendanceIdModel(models.Model):
    date = models.DateField()
    hour_fk = models.ForeignKey(HourModel, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectModel, on_delete=models.CASCADE)

    status_choice = (('reject', 'Reject'),
                     ('cancel', 'Cancel'), ('calloff', 'Call Off'))
    status = models.CharField(max_length=10, choices=status_choice, blank=True)
    hour = models.PositiveIntegerField(choices=hour_choices)

    class Meta:
        db_table = 'attendanceID'
        verbose_name = 'AttendanceID'
        verbose_name_plural = 'AttendancesIDs'


class AttendanceModel(models.Model):
    attendance_id = models.PositiveIntegerField()
    rollno = models.CharField(max_length=10)
    status = models.CharField(max_length=10)  # Present/Absent

    class Meta:
        db_table = 'attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
