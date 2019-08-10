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


class MarkedUrl(models.Model):
    """
    model will hold marked url details
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=1500, verbose_name="Url")
    marked = models.BooleanField(default=True, verbose_name="Is Marked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)