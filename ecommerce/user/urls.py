from django.conf.urls import url, include
from django.contrib import admin
from .views import (
	home, login_page, signup_page, about, contact, logout_page, profile, update, guest_register_view)

urlpatterns = [
    url(r'^$', home),
    url(r'^login/$', login_page),
    url(r'^signup/$', signup_page),
    url(r'^guest_register/$', guest_register_view),
    url(r'^about/$', about),
    url(r'^contact/$', contact),
    url(r'^logout/$', logout_page),
    url(r'^profile/$', profile),
    url(r'^update/$', update),
]

