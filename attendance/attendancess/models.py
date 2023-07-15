from django.db import models

from subject.models import SubjectModel, HourModel
from classroom.models import ClassroomModel

hour_choices = (
    (1, 'I'),
    (2, 'II'),
    (3, 'III'),
    (4, 'IV'),
    (5, 'V')
)

day_order_choices = (
    (1, 'I'),
    (2, 'II'),
    (3, 'III'),
    (4, 'IV'),
    (5, 'V'),
    (6, 'VI')
)


class DayOrderModel(models.Model):
    order = models.PositiveIntegerField(choices=day_order_choices)
    date = models.DateField()

    class Meta:
        db_table = 'dayorder'
        verbose_name = 'Day Order'
        verbose_name_plural = 'Day Orders'


class LeaveDateModel(models.Model):
    leave_date = models.DateField()
    name = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        db_table = 'leavedate'
        verbose_name = 'Leave Date'
        verbose_name_plural = 'Leave Dates'


class AttendanceIdModel(models.Model):
    date = models.DateField()
    hour_fk = models.ForeignKey(HourModel, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectModel, on_delete=models.CASCADE)
    status_choice = (('reject', 'Reject'),
                     ('cancel', 'Cancel'), ('calloff', 'Call Off'))
    status = models.CharField(max_length=10, choices=status_choice, blank=True)
    hour = models.PositiveIntegerField(choices=hour_choices)
    classroom = models.ForeignKey(
        ClassroomModel, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'attendanceID'
        verbose_name = 'AttendanceID'
        verbose_name_plural = 'AttendancesIDs'


class AttendanceModel(models.Model):
    attendance_id = models.ForeignKey(
        AttendanceIdModel, on_delete=models.PROTECT)
    rollno = models.CharField(max_length=10)
    status = models.CharField(max_length=10)  # Present/Absent

    class Meta:
        db_table = 'attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
