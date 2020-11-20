from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	user_type_choice = ((1,'Admin'),(2,'Staff'),(3,'Student'))
	user_type = models.PositiveSmallIntegerField(choices=user_type_choice)

	#required during createsuperuser command
	REQUIRED_FIELDS = ['user_type']