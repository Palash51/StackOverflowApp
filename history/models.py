from django.db import models

# Create your models here.
from searchapp.models import User


class UserHistory(models.Model):
    """model to have user history"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=1500, verbose_name="Url")
    title = models.CharField(max_length=1500, verbose_name="title")
    visit_count = models.IntegerField(null=True, blank=True)
    last_visit_time = models.DateTimeField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_last_visit_time_formate(self):
        return self.last_visit_time.strftime('%d-%m-%Y')
