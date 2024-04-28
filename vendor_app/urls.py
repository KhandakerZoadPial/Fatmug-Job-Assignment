from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendors, name='vendors'),
    path('<int:vendor_id>', views.vendors, name='vendors'),
    path('<int:vendor_id>/performance', views.vendor_performance, name='vendor_performance')
]
