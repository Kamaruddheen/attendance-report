from django.db import models
from subject_module.models import Subject
from classroom.models import ClassroomModel

# Create your models here.

class TimeTable(models.Model):
	set_name = models.CharField(max_length=50)
	hour = models.PositiveSmallIntegerField()
	day = models.CharField(max_length=15)
	sub = models.ForeignKey(Subject,on_delete=models.PROTECT)
	classroom = models.ForeignKey(ClassroomModel,on_delete=models.CASCADE)