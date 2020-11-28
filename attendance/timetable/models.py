from django.db import models
from classroom.models import ClassroomModel

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


class TimetableModel(models.Model):
	hour = models.PositiveSmallIntegerField()
	day = models.CharField(max_length=15)
	subject = models.CharField(max_length=50)
	set_name = models.ForeignKey(TimetablesetModel,on_delete=models.CASCADE)	
	
	class Meta:
		db_table = 'timetable'
		verbose_name = 'Timetable'
		verbose_name_plural = 'Timetables'