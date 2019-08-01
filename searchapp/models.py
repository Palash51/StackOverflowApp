from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
  """
  Model holding the details of users
  """
  mobile_number = models.CharField(max_length=12, null=False)


  def __str__(self):
    return self.email