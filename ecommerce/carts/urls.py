from django.conf.urls import url, include
from .views import cart_home, update, checkout_home, checkout_done_view


app_name = "carts"
urlpatterns = [
    url(r'^$', cart_home, name='home'),
    url(r'^update_details/$', update, name='update'),
    url(r'^checkout/$', checkout_home, name='checkout'),
    url(r'^checkout/success/$', checkout_done_view, name='success'),

    
]

