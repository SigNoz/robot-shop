from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('uniqueid', views.uniqueid, name='uniqueid'),
    path('check/<id>/', views.checkId, name='checkId'),

]
