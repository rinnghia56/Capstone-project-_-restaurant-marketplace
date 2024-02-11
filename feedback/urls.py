from django.urls import path, include
from . import views


urlpatterns = [
    path('add-feedback/<int:fooditem_id>/',views.add_feedback, name='add_feedback'),
    path('add-rating/<int:fooditem_id>/',views.add_rating, name='add_rating'),
]