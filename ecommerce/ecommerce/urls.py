"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from carts.views import cart_detail_api_view
from billing.views import payment_method_view, payment_method_createview

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'checkout/address/create/', checkout_address_create_view, name="checkout_address_create"),
    path(r'checkout/address/reuse/', checkout_address_reuse_view, name="checkout_address_reuse"),
    path(r'api/cart/', cart_detail_api_view, name="api-cart"),
    path(r'billing/payment-method/', payment_method_view, name="billing-payment-method"),
    path(r'billing/payment-method/create/', payment_method_createview, name="billing-payment-method-endpoint"),
    path('', include('user.urls')),
    path('', include('products.urls')),
    path('search/', include('search.urls')),
    path('cart/', include('carts.urls', namespace="cart")),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)