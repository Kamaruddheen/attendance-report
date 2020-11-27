from django.conf import settings
from django.db import models


class AttendanceModel(models.Model):
    date = models.DateField()
    subject = models.CharField(max_length=50)
    handled_by = models.CharField(max_length=150)  # username max length
    status_choice = (('reject', 'Reject'),
                     ('cancel', 'Cancel'), ('calloff', 'Call Off'))
    status = models.CharField(max_length=10, choices=status_choice, blank=True)
    student = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'user_type': 3},
        related_name="student_attendance")

    class Meta:
        db_table = 'attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
