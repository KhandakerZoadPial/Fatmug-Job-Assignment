from django.urls import path
from . import views

urlpatterns = [
    path('', views.purchase_orders, name='purchase_orders'),
    path('<int:po_id>', views.purchase_orders, name='purchase_orders'),
    path('<int:po_id>/acknowledge', views.acknowledge, name='acknowledge')
]
