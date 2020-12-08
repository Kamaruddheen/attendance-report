from django.db import models
from classroom.models import ClassroomModel

from subject.models import SubjectModel
# Create your models here.

class TimetablesetModel(models.Model):
	name = models.CharField(max_length=50, blank=True)
	classroom = models.ForeignKey(ClassroomModel,on_delete=models.CASCADE)
	from_date = models.DateField()
	to_date = models.DateField()
	# is_enabled = models.BooleanField() # ! do we need this [not yet migrated this field]

	class Meta:
		db_table = 'set'
		verbose_name = 'Set'
		verbose_name_plural = 'Sets'

day_choices=(
    (1,'Monday'),
    (2,'Tuesday'),
    (3,'Wednesday'),
    (4,'Thursday'),
    (5,'Friday'),
    (6,'Saturday')
)

hour_choices=(
	(1,'I'),
	(2,'II'),
	(3,'III'),
	(4,'IV'),
	(5,'V')
)

class TimetableModel(models.Model):
	hour = models.CharField(max_length=3,choices=hour_choices)
	day = models.CharField(max_length=15,choices=day_choices)
	subject = models.ForeignKey(SubjectModel, on_delete=models.CASCADE)
	set_name = models.ForeignKey(TimetablesetModel,on_delete=models.CASCADE,help_text='Create a set if your set is not in the choice list')	
	
	class Meta:
		db_table = 'timetable'
		verbose_name = 'Timetable'
		verbose_name_plural = 'Timetables'
