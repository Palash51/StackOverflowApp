from django.contrib import admin
from django.urls import path

from history import views

app_name = 'history'

urlpatterns = [

    path('v1/history', views.UserHistoryAPIView.as_view(), name='marked'),
    path('v1/dashboard', views.DashboardAPIView.as_view(), name='dashboard'),
    path('v1/search/question', views.SearchQuestionAPIView.as_view(), name='search_question')

]
