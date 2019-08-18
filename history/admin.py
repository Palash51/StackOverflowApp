from django.contrib import admin

# Register your models here.
from history.models import UserHistory, BrowsedUrlDetail

admin.site.register(UserHistory)
admin.site.register(BrowsedUrlDetail)