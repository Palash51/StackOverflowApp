from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('searchapp.urls', namespace='search-app')),
    path('', include('history.urls', namespace='history-app')),
    path('', include('chat.urls', namespace='chat-app'))
]
