from django.contrib.auth.models import AbstractUser
from django.db import models
import re
from history.search import MarkedUrlIndex
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
    title = models.CharField(max_length=1500, null=True, blank=True)
    marked = models.BooleanField(default=True, verbose_name="Is Marked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        try:
            question_id = [i for i in re.findall('\d+', self.url) if len(i) > 4][0]
            return "Question ID: {0}".format(question_id)
        except Exception:
            return self.url

    @property
    def get_created_at_time_formate(self):
        return self.created_at.strftime('%d-%m-%Y')

    def indexing(self):
        obj = MarkedUrlIndex(
            meta={'id': self.id},
            user=self.user.username,
            url=self.url,
            title=self.title,
            created_at=self.created_at,

        )
        obj.save()
        return obj.to_dict(include_meta=True)