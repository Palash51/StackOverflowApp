from django.contrib import admin
from django.urls import path

from searchapp import views

app_name = 'searchapp'

urlpatterns = [

    path('v1/signup', views.Signup.as_view(), name='signup'),
    path('v1/signin', views.signin, name='signin'),
    path('v1/signout', views.signout, name='signout'),
    path('v1/search', views.SearchView.as_view(), name='search'),
    path('v1/marked', views.MarkedLink.as_view(), name='marked'),

]
