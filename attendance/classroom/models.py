from django.db import models
from django.conf import settings

# Create your models here.

class ClassroomModel(models.Model):
	course = models.CharField(max_length=50)
	year = models.PositiveSmallIntegerField(choices=((1,'I'),(2,'II'),(3,'III')))
	sec = models.CharField(choices=(('a','A'),('b','B')),null=True,max_length=5)
	tutor = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete = models.PROTECT,
		limit_choices_to=models.Q(user_type=2)|models.Q(user_type=3))
	timetable = models.CharField(null=True,blank=True,max_length=5)