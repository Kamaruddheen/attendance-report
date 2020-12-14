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
	
	def __str__(self):
		return str(self.classroom) + "\n" +  "(" + str(self.from_date) + " - " + str(self.to_date) + ")"
#foriegn key data are not string ;they belong to the particular model so we have to convert that to string to concatenate with the string 
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
	hour = models.PositiveIntegerField(choices=hour_choices)
	day = models.PositiveIntegerField(choices=day_choices)
	subject = models.ForeignKey(SubjectModel, on_delete=models.CASCADE)
	set_name = models.ForeignKey(TimetablesetModel,on_delete=models.CASCADE)
	
	class Meta:
		db_table = 'timetable'
		verbose_name = 'Timetable'
		verbose_name_plural = 'Timetables'
    
	def __str__(self):
		return self.subject.hour_name