from django.urls import path, include
from . import views

urlpatterns = [
    # View list blog
    path('',views.list_blog,name = 'list_blog'),
    # View list blog by category
    path('post_by_category/<slug:category_slug>/',views.list_blog_by_category,name = 'list_blog_by_category'),
    # Post detail
    path('post_detail/<slug:post_slug>/', views.post_detail, name='post_detail'),
]
