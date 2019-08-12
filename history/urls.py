from django.contrib import admin
from django.urls import path

from history import views

app_name = 'history'

urlpatterns = [

    path('v1/history', views.UserHistoryAPIView.as_view(), name='marked'),

]
