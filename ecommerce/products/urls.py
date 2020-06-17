from django.conf.urls import url, include
from django.contrib import admin
from .views import pro, pro_details

urlpatterns = [
    url(r'^electronics/$', pro, {'value':'ER'}),
    url(r'^clothes/$', pro, {'value':'CL'}),
    url(r'^furniture/$', pro, {'value':'FR'}),
    url(r'^furniture/(?P<pk>\d+)/$', pro_details),
    url(r'^electronics/(?P<pk>\d+)/$', pro_details),
    url(r'^clothes/(?P<pk>\d+)/$', pro_details),
]

