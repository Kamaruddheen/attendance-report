from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.

class User(AbstractUser):
	user_type_choice = ((1,'Admin'),(2,'Staff'),(3,'Student'))
	user_type = models.PositiveSmallIntegerField(choices=user_type_choice)

	#required during createsuperuser command
	REQUIRED_FIELDS = ['user_type']

# class StaffModel(models.Model):
# 	user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.PROTECT,
#         limit_choices_to=models.Q(user_type=2))
# 	is_hod = models.BooleanField(default=False)

# 	class Meta:		
# 		db_table = 'staff'
# 		verbose_name = 'Staff'
# 		verbose_name_plural = 'Staffs'

# @receiver(post_save, sender=User)
# def create_user_staffmodel(sender, instance, created, **kwargs):
#     if created:
#         StaffModel.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_staffmodel(sender, instance, **kwargs):
#     instance.staffmodel.save()