from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace,name='marketplace'),
    # List food
    path('food/',views.list_food, name='list_food_for_customer'),
    path('menu/<slug:category_default_slug>', views.list_food_by_menu_default, name='list_food_by_menu_default'),

    # Favorite
    path('foods_favorite/', views.foods_favorite, name='foods_favorite'),
    path('get_foods_favorite/', views.get_foods_favorite, name ='get_foods_favorite'),
    path('add_food_favorite/<int:food_id>/', views.add_food_favorite, name = 'add_food_favorite'),
    path('remove_food_favorite/<int:food_favorite_id>/', views.remove_food_favorite, name = 'remove_food_favorite'),

    # Detail restaurant and food
    path('food_detail/<slug:food_slug>', views.food_detail, name='food_detail'),
    path('vendor_detail/<slug:vendor_slug>/', views.vendor_details, name='vendor_detail'),
    path('vendor_detail_by_menu/<slug:vendor_slug>/<slug:category_slug>/', views.vendor_details_by_menu, name='vendor_details_by_menu'),
   
    # Cart
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease_cart/<int:food_id>/', views.decrease_cart, name='decrease_cart'),
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),
]
