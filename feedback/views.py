from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment, Rating
from menu.models import FoodItem
from .forms import CommentForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.db.models import Avg
from math import floor
from .utils import my_predict


# Create your views here.
def add_feedback(request, fooditem_id):
    if request.user.is_authenticated:
            food_item = get_object_or_404(FoodItem, id=fooditem_id)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
                form = CommentForm(request.POST)

                if form.is_valid():
                    comment = Comment.objects.create(
                        food_item=food_item,
                        user=request.user,
                        text=form.cleaned_data['text'],
                        sentiment = my_predict([form.cleaned_data['text']])
                    )

                    comment_current = Comment.objects.get(pk=comment.id)

                    picture = comment_current.user.userprofile.profile_picture.url if comment_current.user.userprofile.profile_picture else ""

                        
                    data = {
                        'status': 'success',
                        'message': 'Comment added successfully.',
                        'comment_content': comment.text,
                        'comment_user': (comment.user.first_name + comment.user.last_name),
                        'comment_date': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'picture': picture,
                    }
                        
                    return JsonResponse(data)
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

def calculate_avg_rating(fooditem):
    ordered_users = User.objects.filter(orderedfood__fooditem__slug=fooditem.slug).distinct()
    if ordered_users.count() > 0:
        avg_rating = Rating.objects.filter(food_item=fooditem, user__in=ordered_users).aggregate(avg_rating=Avg('value'))
        if avg_rating['avg_rating'] is not None:
                avg_rating_rounded = floor(avg_rating['avg_rating'])
                fooditem.rating = avg_rating_rounded
                fooditem.rating_count = ordered_users.count()
                fooditem.save()

def add_rating(request, fooditem_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            try:
                fooditem = FoodItem.objects.get(id=fooditem_id)
                try:
                    rating = Rating.objects.get(food_item=fooditem, user=request.user)
                    rating_value = request.POST.get('rating')
                    rating.value = rating_value
                    rating.save()
                    calculate_avg_rating(fooditem)
                    return JsonResponse({'status': 'success','message': 'Updated rating success'})
                except:
                    rating_value = request.POST.get('rating')
                    rating = Rating.objects.create(food_item=fooditem, user=request.user, value=rating_value)
                    calculate_avg_rating(fooditem)
                    return JsonResponse({'status': 'Success', 'message': 'Thank you for your review'})
            except Exception as e:
                print(f"Lỗi xảy ra: {e}")
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


    
