from django.contrib import admin

# Register your models here.
from history.models import UserHistory

admin.site.register(UserHistory)