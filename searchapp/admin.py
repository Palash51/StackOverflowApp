from django.contrib import admin

from searchapp.models import User, MarkedUrl

admin.site.register(User)
admin.site.register(MarkedUrl)