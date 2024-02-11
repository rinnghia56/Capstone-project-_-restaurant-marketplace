from django.urls import path
from accounts import views as AccountViews
from . import views

urlpatterns = [
    path('', AccountViews.cusDashboard, name='customer'),
    # View profile
    path('profile/', views.cprofile, name='cprofile'),
    # View order
    path('my_orders/', views.my_orders, name='customer_my_orders'),
    # View order detail
    path('order_details/<int:order_number>/', views.order_detail, name='order_detail'),
]
