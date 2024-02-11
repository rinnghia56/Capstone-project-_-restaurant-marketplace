from django.shortcuts import render
from blogs.models import Post
from menu.models import FoodItem

def index(request):
    posts = Post.objects.all()[:3]
    foods = FoodItem.objects.filter(is_available=True).order_by('-rating')[:8]
    context = {
        'posts':posts,
        'foods':foods
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')