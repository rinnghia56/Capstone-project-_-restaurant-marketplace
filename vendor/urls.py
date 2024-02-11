from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.venDashboard, name='vendor'),
    path('profile/',views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),

    # Category CRUD
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # FoodItem CRUD
    path('menu-builder/food/add/', views.add_food, name='add_food'),
    path('menu-builder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),


    # FoodImage CRUD
    path('food-image/<int:pk>/', views.foodimages_by_fooditem, name='view_image'),
    path('food-image/add-image/<int:pk>/', views.add_image, name='add_image_food'),
    path('food-image/delete-image/<int:pk>/', views.delete_image, name='delete_image_food'),

    # Opening Hour CRUD
    path('opening-hours/', views.opening_hours, name='opening_hours'),
    path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>/', views.remove_opening_hours, name='remove_opening_hours'),

    # Order
    path('order_detail/<int:order_number>/', views.order_detail, name='vendor_order_detail'),
    path('my_orders/', views.my_orders, name='vendor_my_orders'),

    # Sentiment
    path('sentiment_comment/',views.sentiment_comment, name="vendor_sentiment_comment"),
    path('view_comment/<int:food_id>/',views.view_comment_by_sentiment, name="vendor_view_comment_by_sentiment"),
    path('view_all_comment/',views.view_all_comment_by_sentiment, name = 'view_all_comment_by_sentiment'),

    # Post
    path('manage_post/', views.manage_post, name='manage_post'),
    path('manage_post/add/', views.add_post, name='add_post'),
    path('manage_post/edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('manage_post/delete/<int:pk>/', views.delete_post, name='delete_post'),
]
