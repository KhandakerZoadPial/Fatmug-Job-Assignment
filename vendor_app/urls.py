from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_vendors, name='all_vendors'),
    path('create', views.create_vendor, name='create_vendor'),
    path('retrieve_vendor/<int:vendor_id>', views.retrieve_vendor, name='retrieve_vendor'),
    path('update_vendor/<int:vendor_id>', views.update_vendor, name='update_vendor'),
    path('delete_vendor/<int:vendor_id>', views.delete_vendor, name='delete_vendor')
]
