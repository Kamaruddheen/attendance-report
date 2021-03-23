from django.db import models
from django.conf import settings
from django.urls import reverse
from classroom.models import ClassroomModel


class HourModel(models.Model):
    name = models.CharField(max_length=50)
    classroom = models.ForeignKey(ClassroomModel,on_delete=models.CASCADE)
    hour_type = models.CharField(max_length=10,choices=(('reg','Regular'),('sel','Selective'),('lab','Lab')))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subject:hour_detail',args=[self.classroom.id,self.id])

    def get_edit_url(self):
        return reverse('subject:edit_hour',args=[self.classroom.id,self.id])

    # class Meta:
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['name', 'classroom'], name="unique_sub_per_class")
        # ]

# Create your models here.
class SubjectModel(models.Model):
    # hour_name = models.CharField(max_length=50)
    sub_name = models.CharField(max_length=50)
    hour = models.ForeignKey(HourModel,on_delete=models.CASCADE,null=True)
    handled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to=models.Q(user_type=2))
    # classroom = models.ForeignKey(
    #     ClassroomModel,
    #     on_delete=models.CASCADE)
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'user_type': 3},
        related_name="students",
        blank=True) #null=True is not required for manytomany field, just blank will do
    
    def __str__(self):
        return self.sub_name

    def get_add_student_url(self):
        return reverse('subject:hour_add_students',args=[self.hour.classroom.id,self.hour.id,self.id])

    class Meta:
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['sub_name', 'classroom'], name="unique_sub_per_class")
        # ]
        db_table = 'subject'
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    

