from django.db import models
from subject.models import SubjectModel
from classroom.models import ClassroomModel

# Create your models here.

class TimetableModel(models.Model):
	set_name = models.CharField(max_length=50)
	hour = models.PositiveSmallIntegerField()
	day = models.CharField(max_length=15)
	sub = models.ForeignKey(SubjectModel,on_delete=models.PROTECT)
	classroom = models.ForeignKey(ClassroomModel,on_delete=models.CASCADE)
	
	class Meta:
		db_table = 'timetable'
		verbose_name = 'Timetable'
		verbose_name_plural = 'Timetables'