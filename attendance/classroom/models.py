from django.db import models
from django.conf import settings

# Create your models here.

class ClassroomModel(models.Model):
	course = models.CharField(max_length=50)
	year = models.PositiveSmallIntegerField(choices=((1,'I'),(2,'II'),(3,'III')))
	sec = models.CharField(choices=(('a','A'),('b','B')),null=True,blank=True,max_length=5)
	tutor = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete = models.PROTECT,
		limit_choices_to={'user_type':2})

	class Meta:
		verbose_name = 'Classroom'
		verbose_name_plural = 'Classrooms'