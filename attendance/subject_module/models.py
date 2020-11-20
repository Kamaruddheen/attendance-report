from django.db import models
from django.conf import settings
from classroom.models import ClassroomModel

# Create your models here.

class Subject(models.Model):
	hour_name = models.CharField(max_length=50)
	sub_name = models.CharField(max_length=50)
	sub_type = models.CharField(max_length=10,choices=(('reg','Regular'),('sel','Selective')))
	handled_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete = models.PROTECT,
		limit_choices_to=models.Q(user_type=2))
	classroom = models.ForeignKey(
		ClassroomModel,
		on_delete = models.CASCADE)
	students = models.ManyToManyField(
		settings.AUTH_USER_MODEL,
		limit_choices_to={'user_type':3},
		related_name = "students",
		blank=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['sub_name','classroom'], name = "unique_sub_per_class")
		]